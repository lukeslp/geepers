# Sortable Table with aria-sort

**Category**: accessibility
**Source**: html/datavis/billions/script_v2.js + styles.css (2026-03-08)
**Tags**: a11y, aria-sort, sortable-table, wcag, keyboard

## Problem

Sortable data tables that update `aria-sort` attributes need to do it correctly: one column at a time, always on the `<th>`, with `"none"` on all non-active columns, and a visible indicator that's hidden from screen readers.

## Pattern — JS

```javascript
let currentSort = { column: 'rank', direction: 'asc' };

function sortEntities(column) {
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'asc';
    }

    filteredEntities.sort((a, b) => {
        let valA, valB;
        switch (column) {
            case 'rank':  valA = a.rank;  valB = b.rank;  break;
            case 'name':  valA = a.name.toLowerCase(); valB = b.name.toLowerCase(); break;
            case 'value': valA = a.value; valB = b.value; break;
            default:      valA = a.rank;  valB = b.rank;
        }
        const cmp = typeof valA === 'string' ? valA.localeCompare(valB) : valA - valB;
        return currentSort.direction === 'desc' ? -cmp : cmp;
    });

    currentPage = 1;
    renderTable();
    updateSortIndicators();
}

function updateSortIndicators() {
    const headers = document.querySelectorAll('#my-table thead th');
    const columns = ['rank', 'name', 'value', 'type'];

    headers.forEach((th, i) => {
        // Remove previous indicator
        th.querySelector('.sort-indicator')?.remove();

        th.setAttribute('aria-sort', columns[i] === currentSort.column
            ? (currentSort.direction === 'asc' ? 'ascending' : 'descending')
            : 'none');

        if (columns[i] === currentSort.column) {
            const indicator = document.createElement('span');
            indicator.className = 'sort-indicator';
            indicator.textContent = currentSort.direction === 'asc' ? ' \u25B2' : ' \u25BC';
            indicator.setAttribute('aria-hidden', 'true'); // screen readers get aria-sort instead
            th.appendChild(indicator);
        }
    });
}
```

## Pattern — HTML

```html
<table id="my-table">
  <thead>
    <tr>
      <!-- tabindex="0" + role="columnheader" allows keyboard activation -->
      <th scope="col" role="columnheader" tabindex="0"
          aria-sort="ascending" onclick="sortEntities('rank')"
          onkeydown="if(event.key==='Enter'||event.key===' ')sortEntities('rank')">
        Rank
      </th>
      <th scope="col" role="columnheader" tabindex="0"
          aria-sort="none" onclick="sortEntities('name')"
          onkeydown="if(event.key==='Enter'||event.key===' ')sortEntities('name')">
        Name
      </th>
    </tr>
  </thead>
</table>
```

## Pattern — CSS

```css
thead th {
  cursor: pointer;
  user-select: none;
}
thead th:focus-visible {
  outline: 3px solid var(--focus-ring-color);
  outline-offset: -2px;
}
.sort-indicator {
  font-size: 0.75em;
  margin-left: 0.25em;
}
```

## WCAG compliance

- `aria-sort` on `<th>` satisfies 4.1.2 (Name, Role, Value)
- `aria-hidden="true"` on the visual indicator prevents double-announcement
- `scope="col"` satisfies 1.3.1 (Info and Relationships)
- `:focus-visible` outline satisfies 2.4.7 (Focus Visible)
- Enter/Space keydown handler satisfies 2.1.1 (Keyboard)
