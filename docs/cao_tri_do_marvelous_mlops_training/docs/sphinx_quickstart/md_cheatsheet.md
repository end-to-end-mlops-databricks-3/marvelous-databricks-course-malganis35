# Markdown Cheat Sheet

Source: https://github.com/canonical/data-science-stack/blob/main/docs/doc-cheat-sheet-myst.md

This file contains the syntax for commonly used Markdown and MyST markup.
Open it in your text editor to quickly copy and paste the markup you need.

Also see the [MyST documentation](https://myst-parser.readthedocs.io/en/latest/index.html) for detailed information, and the [Canonical Documentation Style Guide](https://docs.ubuntu.com/styleguide/en) for general style conventions.

## H2 heading

### H3 heading

#### H4 heading

##### H5 heading

## Inline formatting

- {guilabel}`UI element`
- `code`
- {command}`command`
- {kbd}`Key`
- *Italic*
- **Bold**

## Code blocks

Start a code block:

    code:
      - example: true

```
# Demonstrate a code block
code:
  - example: true
```

```yaml
# Demonstrate a code block
code:
  - example: true
```

(a_section_target_myst)=
## Links

- [Canonical website](https://canonical.com/)
- https:/<span></span>/canonical.com/
- {ref}`a_section_target_myst`
- {ref}`Link text <a_section_target_myst>`
- {doc}`index`
- {doc}`Link text <index>`


## Navigation

Use the following syntax::

    ```{toctree}
    :hidden:

    sub-page1
    sub-page2
    ```

## Lists

1. Step 1
   - Item 1
     * Sub-item
   - Item 2
     1. Sub-step 1
     1. Sub-step 2
1. Step 2
   1. Sub-step 1
      - Item
   1. Sub-step 2

Term 1
: Definition

Term 2
: Definition

## Tables

## Markdown tables

| Header 1                           | Header 2 |
|------------------------------------|----------|
| Cell 1<br>Second paragraph         | Cell 2   |
| Cell 3                             | Cell 4   |

Centred:

| Header 1                           | Header 2 |
|:----------------------------------:|:--------:|
| Cell 1<br>Second paragraph         | Cell 2   |
| Cell 3                             | Cell 4   |

## List tables

```{list-table}
   :header-rows: 1

* - Header 1
  - Header 2
* - Cell 1

    Second paragraph
  - Cell 2
* - Cell 3
  - Cell 4
```

Centred:

```{list-table}
   :header-rows: 1
   :align: center

* - Header 1
  - Header 2
* - Cell 1

    Second paragraph
  - Cell 2
* - Cell 3
  - Cell 4
```

## Notes

```{note}
A note.
```

```{tip}
A tip.
```

```{important}
Important information
```

```{caution}
This might damage your hardware!
```

## Images

![Alt text](https://assets.ubuntu.com/v1/b3b72cb2-canonical-logo-166.png)

```{figure} https://assets.ubuntu.com/v1/b3b72cb2-canonical-logo-166.png
   :width: 100px
   :alt: Alt text

   Figure caption
```

## Reuse

### Keys

Keys can be defined at the top of a file, or in a `myst_substitutions` option in `conf.py`.

{{reuse_key}}

{{advanced_reuse_key}}

### File inclusion

```{include} index.rst
   :start-after: include_start
   :end-before: include_end
```

## Glossary

```{glossary}

some term
  Definition of the example term.
```

{term}`some term`

## More useful markup

- ```{versionadded} X.Y
- {abbr}`API (Application Programming Interface)`
