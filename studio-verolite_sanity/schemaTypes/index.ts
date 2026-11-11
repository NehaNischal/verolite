import { defineField, defineType } from 'sanity'
import { createVariantFieldComponent } from './VariantField'
import { categoryGroup } from './categoryGroup'
import { category } from './category'

export const product = defineType({
    name: 'product',
    title: 'Product',
    type: 'document',

    fields: [
        // Basic information
        defineField({
            name: 'name',
            title: 'Product Name',
            type: 'string',
            validation: (Rule) => Rule.required(),
        }),

        defineField({
            name: 'model',
            title: 'Model',
            type: 'string',
            validation: (Rule) => Rule.required(),
        }),

        defineField({
            name: 'slug',
            title: 'URL Slug',
            type: 'slug',
            options: {
                source: 'name',
                maxLength: 96,
            },
            validation: (Rule) => Rule.required(),
        }),

        defineField({
            name: 'category',
            title: 'Subcategory (Website Category)',
            type: 'reference',
            to: [{ type: 'category' }],
            description: 'Select an existing category or click "+ Create new" to add a new category.',
            validation: (Rule) => Rule.required(),
        }),

        defineField({
            name: 'shortDescription',
            title: 'Short Description',
            type: 'text',
            rows: 3,
        }),

        defineField({
            name: 'description',
            title: 'Product Description',
            type: 'text',
            rows: 6,
        }),

        // Images
        defineField({
            name: 'mainImage',
            title: 'Main Product Image',
            type: 'image',
            options: {
                hotspot: true,
            },
        }),

        defineField({
            name: 'gallery',
            title: 'Product Gallery',
            type: 'array',
            of: [
                {
                    type: 'image',
                    options: {
                        hotspot: true,
                    },
                },
            ],
        }),

        // Features
        defineField({
            name: 'features',
            title: 'Features',
            type: 'array',
            of: [{ type: 'string' }],
        }),

        // Technical specifications
        defineField({
            name: 'specifications',
            title: 'Technical Specifications',
            type: 'array',
            of: [
                {
                    type: 'object',
                    fields: [
                        {
                            name: 'label',
                            title: 'Specification',
                            type: 'string',
                        },
                        {
                            name: 'value',
                            title: 'Value',
                            type: 'string',
                        },
                    ],
                    preview: {
                        select: {
                            title: 'label',
                            subtitle: 'value',
                        },
                    },
                },
            ],
        }),

        // Variant Table Column Headers configuration
        defineField({
            name: 'variantHeaders',
            title: 'Variant Table Columns & Headers',
            description:
                'Customize or rename table column headers for this product. If a column is not needed (e.g. no CCT or Cut-Out), leave it blank or type "-" to hide that column completely from the variant editor and website table.',
            type: 'object',
            options: {
                collapsible: true,
                collapsed: false,
                columns: 2,
            },
            fields: [
                defineField({
                    name: 'col1',
                    title: 'Column 1 Header (Default: Model)',
                    type: 'string',
                    initialValue: 'Model',
                    placeholder: 'e.g. Model, SKU, Item Code',
                }),
                defineField({
                    name: 'col2',
                    title: 'Column 2 Header (Default: Wattage)',
                    type: 'string',
                    initialValue: 'Wattage',
                    placeholder: 'e.g. Wattage, Output Power, Voltage',
                }),
                defineField({
                    name: 'col3',
                    title: 'Column 3 Header (Default: CCT)',
                    type: 'string',
                    initialValue: 'CCT',
                    placeholder: 'e.g. CCT, Color, Output Current',
                }),
                defineField({
                    name: 'col4',
                    title: 'Column 4 Header (Default: Body)',
                    type: 'string',
                    initialValue: 'Body',
                    placeholder: 'e.g. Body, Finish, Dimming Type',
                }),
                defineField({
                    name: 'col5',
                    title: 'Column 5 Header (Default: Size)',
                    type: 'string',
                    initialValue: 'Size',
                    placeholder: 'e.g. Size, Dimensions, Length',
                }),
                defineField({
                    name: 'col6',
                    title: 'Column 6 Header (Default: Cut-Out)',
                    type: 'string',
                    initialValue: 'Cut-Out',
                    placeholder: 'e.g. Cut-Out, IP Rating, Beam Angle',
                }),
            ],
        }),

        // Product variants
        defineField({
            name: 'variants',
            title: 'Product Variants',
            description:
                'Add product variants/models. Field labels dynamically match the column headers defined above.',
            type: 'array',
            of: [
                {
                    type: 'object',
                    fields: [
                        {
                            name: 'model',
                            title: 'Model',
                            type: 'string',
                            components: {
                                field: createVariantFieldComponent('col1', 'Model'),
                            },
                        },
                        {
                            name: 'wattage',
                            title: 'Wattage',
                            type: 'string',
                            components: {
                                field: createVariantFieldComponent('col2', 'Wattage'),
                            },
                        },
                        {
                            name: 'cct',
                            title: 'CCT',
                            type: 'string',
                            components: {
                                field: createVariantFieldComponent('col3', 'CCT'),
                            },
                        },
                        {
                            name: 'body',
                            title: 'Body',
                            type: 'string',
                            components: {
                                field: createVariantFieldComponent('col4', 'Body'),
                            },
                        },
                        {
                            name: 'size',
                            title: 'Size',
                            type: 'string',
                            components: {
                                field: createVariantFieldComponent('col5', 'Size'),
                            },
                        },
                        {
                            name: 'cutOut',
                            title: 'Cut-out',
                            type: 'string',
                            components: {
                                field: createVariantFieldComponent('col6', 'Cut-Out'),
                            },
                        },
                        {
                            name: 'pdf',
                            title: 'Variant PDF / Datasheet',
                            type: 'file',
                        },
                    ],
                    preview: {
                        select: {
                            model: 'model',
                            wattage: 'wattage',
                            cct: 'cct',
                            body: 'body',
                            size: 'size',
                            cutOut: 'cutOut',
                        },
                        prepare(selection) {
                            const { model, wattage, cct, body, size, cutOut } = selection
                            const details = [wattage, cct, body, size, cutOut]
                                .filter(Boolean)
                                .join(' | ')
                            return {
                                title: model || 'Untitled Variant',
                                subtitle: details || 'No details entered',
                            }
                        },
                    },
                },
            ],
        }),

        // Main product PDF
        defineField({
            name: 'datasheet',
            title: 'Product Datasheet / PDF',
            type: 'file',
        }),

        // Search Engine Optimization (SEO) & Social Sharing Metadata
        defineField({
            name: 'seoTitle',
            title: 'SEO Title (Page Title)',
            type: 'string',
            description: 'Custom browser page title (recommended: 50-60 characters). If left blank, automatically falls back to: "[Product Name] ([Model]) | VEROLITE Architectural Lighting".',
            validation: (Rule) => Rule.max(70).warning('Titles longer than 60-70 characters may be truncated in search results.'),
        }),

        defineField({
            name: 'seoDescription',
            title: 'SEO Meta Description',
            type: 'text',
            rows: 3,
            description: 'Summary shown in search engine snippet cards (recommended: 140-160 characters). If left blank, automatically falls back to the luminaire\'s Short Description.',
            validation: (Rule) => Rule.max(180).warning('Descriptions longer than 160 characters may be truncated in Google search snippets.'),
        }),

        defineField({
            name: 'canonicalUrl',
            title: 'Custom Canonical URL',
            type: 'url',
            description: 'Optional custom canonical URL override if this product has an alternate master page. If left blank, automatically defaults to: "https://verolite.co.uk/product.html?slug=[slug]".',
        }),

        defineField({
            name: 'seoImage',
            title: 'Custom Social Share Image (Open Graph / Twitter)',
            type: 'image',
            description: 'Optional social share preview image (1200x630px recommended). If left blank, automatically falls back to Main Product Image.',
            options: {
                hotspot: true,
            },
        }),

        defineField({
            name: 'noIndex',
            title: 'Exclude from Search Engines (noindex)',
            type: 'boolean',
            description: 'Toggle on only if you want search engines to NOT index this product page.',
            initialValue: false,
        }),
    ],

    preview: {
        select: {
            title: 'name',
            subtitle: 'model',
            media: 'mainImage',
        },
    },
})
export const schemaTypes = [product, categoryGroup, category]