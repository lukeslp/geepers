"""
Multi-Provider LLM API Client with Fallback and Provider Switching

Description: Universal LLM integration supporting multiple providers (xAI, OpenAI,
Anthropic) with automatic provider detection, health checking, and graceful fallbacks.
Includes caching, history tracking, and production/development environment detection.

Use Cases:
- AI-powered applications needing flexibility across LLM providers
- Cost optimization by switching between providers
- Resilience through automatic failover
- Testing different models for comparison

Dependencies:
- Modern browser with fetch API
- Backend API proxy recommended for API key security

Notes:
- Detects production vs localhost automatically
- Supports text, image, and video generation (where available)
- Built-in request caching to reduce API calls
- Generation history tracking for debugging
- Graceful degradation with fallback text

Related Snippets:
- See sse-streaming.js for real-time generation streaming
- See api-error-handling.py for backend proxy implementation
"""

class LLMIntegration {
    constructor(apiKey = null) {
        this.apiKey = apiKey;

        // Auto-detect environment
        const isProduction = window.location.hostname === 'dr.eamer.dev';
        this.proxyEndpoint = isProduction
            ? '/campbell/api'  // Caddy reverse proxy
            : 'http://localhost:8000/api'; // Development

        this.currentProvider = 'xai'; // Default provider

        // Provider configurations
        this.providers = {
            xai: {
                name: 'xAI (Grok)',
                models: {
                    text: 'grok-3',
                    image: 'grok-2-image-1212',
                    video: 'grok-2-image-1212'
                }
            },
            openai: {
                name: 'OpenAI (GPT)',
                models: {
                    text: 'gpt-4o',
                    image: 'dall-e-3',
                    video: 'dall-e-3'
                }
            },
            'sonnet-4.5': {
                name: 'Sonnet 4.5 (Claude)',
                models: {
                    text: 'claude-3-5-sonnet-20241022',
                    image: 'claude-3-5-sonnet-20241022',
                    video: 'claude-3-5-sonnet-20241022'
                }
            }
        };

        this.cache = new Map();
        this.generationHistory = [];
        this.isConnected = false;

        // Initialize
        this.testConnection();
        this.loadAvailableProviders();
    }

    // Provider Management
    async loadAvailableProviders() {
        try {
            const response = await fetch(`${this.proxyEndpoint}/providers`);
            const data = await response.json();

            if (data.providers) {
                // Update local provider configs with server data
                for (const [name, config] of Object.entries(data.providers)) {
                    if (this.providers[name]) {
                        this.providers[name].available = config.available;
                        this.providers[name].models = config.models;
                    }
                }

                // Set default provider from server
                if (data.default && this.providers[data.default]) {
                    this.currentProvider = data.default;
                }
            }
        } catch (error) {
            console.warn('Unable to load provider information:', error.message);
        }
    }

    setProvider(providerName) {
        if (this.providers[providerName]) {
            this.currentProvider = providerName;
            console.log(`Switched to provider: ${this.providers[providerName].name}`);
            return true;
        }
        return false;
    }

    getCurrentProvider() {
        return this.currentProvider;
    }

    getAvailableProviders() {
        return Object.entries(this.providers).map(([key, config]) => ({
            key,
            name: config.name,
            available: config.available !== false,
            models: config.models
        }));
    }

    // Connection Testing
    async testConnection(provider = null) {
        const testProvider = provider || this.currentProvider;

        try {
            const response = await fetch(
                `${this.proxyEndpoint}/test?provider=${testProvider}`
            );
            const data = await response.json();

            if (data.success) {
                this.isConnected = true;
                console.log(`${data.provider} API connection successful:`, data.message);
                return { success: true, provider: data.provider, message: data.message };
            } else {
                this.isConnected = false;
                console.warn(`${testProvider} API connection failed:`, data.error);
                return { success: false, provider: testProvider, error: data.error };
            }
        } catch (error) {
            this.isConnected = false;
            console.warn(`Unable to connect to ${testProvider} API proxy:`, error.message);
            return { success: false, provider: testProvider, error: error.message };
        }
    }

    // Text Generation
    async generateText(prompt, systemPrompt = null, options = {}) {
        if (!this.isConnected) {
            console.warn('API not connected, using fallback');
            return this.getFallbackText(prompt);
        }

        const currentModel = this.providers[this.currentProvider]?.models?.text;

        const requestBody = {
            provider: this.currentProvider,
            model: currentModel,
            messages: [
                { role: 'system', content: systemPrompt || 'You are a helpful assistant.' },
                { role: 'user', content: prompt }
            ],
            temperature: options.temperature || 0.8,
            max_tokens: options.maxTokens || 1000,
            stream: false
        };

        try {
            const response = await fetch(`${this.proxyEndpoint}/chat/completions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(
                    `API request failed: ${response.status} - ${errorData.error || 'Unknown error'}`
                );
            }

            const data = await response.json();

            if (!data.choices || !data.choices[0] || !data.choices[0].message) {
                throw new Error('Invalid response format from API');
            }

            const generatedText = data.choices[0].message.content;

            this.addToHistory('text', prompt, generatedText);
            console.log('Text generated successfully');

            return generatedText;
        } catch (error) {
            console.error('Text generation error:', error);
            return this.getFallbackText(prompt);
        }
    }

    // Image Generation
    async generateImage(prompt, style = 'realistic') {
        if (!this.isConnected) {
            console.warn('API not connected, skipping image generation');
            return null;
        }

        const imagePrompt = this.buildImagePrompt(prompt, style);
        const currentModel = this.providers[this.currentProvider]?.models?.image;

        try {
            const response = await fetch(`${this.proxyEndpoint}/images/generations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    provider: this.currentProvider,
                    model: currentModel,
                    prompt: imagePrompt,
                    n: 1,
                    response_format: 'url'
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(
                    `Image generation failed: ${response.status} - ${errorData.error || 'Unknown error'}`
                );
            }

            const data = await response.json();

            if (!data.data || !data.data[0] || !data.data[0].url) {
                throw new Error('Invalid image response format from API');
            }

            const imageUrl = data.data[0].url;

            this.addToHistory('image', prompt, imageUrl);
            console.log('Image generated successfully');

            return imageUrl;
        } catch (error) {
            console.error('Image generation error:', error);
            return null;
        }
    }

    buildImagePrompt(basePrompt, style) {
        const styleGuides = {
            fantasy: 'fantasy art style, detailed, magical atmosphere, epic lighting',
            scifi: 'science fiction art style, futuristic, high-tech, cinematic',
            horror: 'dark atmospheric horror style, moody lighting, unsettling',
            realistic: 'photorealistic, natural lighting, highly detailed',
            artistic: 'artistic style, creative composition, vibrant colors'
        };

        return `${basePrompt}, ${styleGuides[style] || styleGuides.realistic}, high quality, detailed`;
    }

    // Caching
    getCachedGeneration(prompt) {
        return this.cache.get(prompt);
    }

    setCachedGeneration(prompt, result) {
        this.cache.set(prompt, result);

        // Limit cache size to 100 items
        if (this.cache.size > 100) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
    }

    // History
    addToHistory(type, prompt, result) {
        this.generationHistory.push({
            type,
            prompt,
            result,
            timestamp: Date.now(),
            provider: this.currentProvider
        });

        // Keep last 50 generations
        if (this.generationHistory.length > 50) {
            this.generationHistory.shift();
        }
    }

    exportHistory() {
        return {
            generations: this.generationHistory,
            timestamp: Date.now()
        };
    }

    // Fallback for API failures
    getFallbackText(prompt) {
        const fallbacks = {
            default: "Unable to generate content at this time. Please try again later.",
            story: "The adventure continues in unexpected ways...",
            code: "// Code generation unavailable",
            analysis: "Analysis pending - please check back soon."
        };

        // Try to match prompt to fallback
        for (const [key, text] of Object.entries(fallbacks)) {
            if (prompt.toLowerCase().includes(key)) {
                return text;
            }
        }

        return fallbacks.default;
    }
}

// Usage example
if (typeof module === 'undefined') {
    // Browser environment - ready to use
    window.LLMIntegration = LLMIntegration;
} else {
    // Node.js environment - export
    module.exports = LLMIntegration;
}

/*
Example Usage:

// Initialize
const llm = new LLMIntegration();

// Test connection
const status = await llm.testConnection();
if (status.success) {
    console.log('Connected to', status.provider);
}

// Generate text
const text = await llm.generateText(
    'Write a short story about a robot',
    'You are a creative storyteller',
    { temperature: 0.9, maxTokens: 500 }
);

// Generate image
const imageUrl = await llm.generateImage(
    'A futuristic cityscape at sunset',
    'scifi'
);

// Switch provider
llm.setProvider('openai');
const gptText = await llm.generateText('Hello, world!');

// Get available providers
const providers = llm.getAvailableProviders();
console.log('Available:', providers.filter(p => p.available));

// Export history for debugging
const history = llm.exportHistory();
console.log('Generated', history.generations.length, 'items');
*/
