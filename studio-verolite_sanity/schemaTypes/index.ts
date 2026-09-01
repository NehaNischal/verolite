import { defineField, defineType } from 'sanity'

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
            title: 'Category',
            type: 'string',
            description: 'Select the website category where this product belongs',
            options: {
                list: [
                    { title: 'Recessed LED Down Lights', value: 'recessed-led-down-lights' },
                    { title: 'LED Surface Down Lights', value: 'led-surface-down-lights' },
                    { title: '3-Phase Track Lights', value: '3phase-track-lights' },
                    { title: 'LED Garden Lights', value: 'led-garden-lights' },
                    { title: 'LED Strip Lights', value: 'led-strip-lights' },
                    { title: 'LED Outdoor Flexible Neon Light', value: 'led-outdoor-flexible-neon-light' },
                    { title: 'LED Magnetic Track Lights', value: 'led-magnetic-track-lights' },
                    { title: 'Office Linear Lights', value: 'office-linear-lights' },
                    { title: 'LED Strip Light Drivers', value: 'led-strip-light-drivers' },
                    { title: 'LED Phase Cut Dimmer', value: 'led-phase-cut-dimmer' },
                    { title: 'LED Sensor Switches', value: 'led-sensor-switches' },
                ],
                layout: 'dropdown',
            },
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

        // Product variants
        defineField({
            name: 'variants',
            title: 'Product Variants',
            type: 'array',
            of: [
                {
                    type: 'object',
                    fields: [
                        {
                            name: 'model',
                            title: 'Model',
                            type: 'string',
                        },
                        {
                            name: 'wattage',
                            title: 'Wattage',
                            type: 'string',
                        },
                        {
                            name: 'cct',
                            title: 'CCT',
                            type: 'string',
                        },
                        {
                            name: 'body',
                            title: 'Body',
                            type: 'string',
                        },
                        {
                            name: 'size',
                            title: 'Size',
                            type: 'string',
                        },
                        {
                            name: 'cutOut',
                            title: 'Cut-out',
                            type: 'string',
                        },
                        {
                            name: 'pdf',
                            title: 'Variant PDF',
                            type: 'file',
                        },
                    ],
                    preview: {
                        select: {
                            title: 'model',
                            subtitle: 'wattage',
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
    ],

    preview: {
        select: {
            title: 'name',
            subtitle: 'model',
            media: 'mainImage',
        },
    },
})
export const schemaTypes = [product]