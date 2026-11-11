import { defineField, defineType } from 'sanity'

export const categoryGroup = defineType({
    name: 'categoryGroup',
    title: 'Primary Category',
    type: 'document',
    fields: [
        defineField({
            name: 'title',
            title: 'Category Name',
            type: 'string',
            description: 'Main category name (e.g. Indoor Lights, Outdoor Lights, Drivers & Controllers, Emergency Lights)',
            validation: (Rule) => Rule.required(),
        }),
        defineField({
            name: 'slug',
            title: 'Slug',
            type: 'slug',
            description: 'URL identifier (e.g. indoor, outdoor, drivers, emergency)',
            options: {
                source: 'title',
                maxLength: 96,
            },
            validation: (Rule) => Rule.required(),
        }),
        defineField({
            name: 'order',
            title: 'Display Order',
            type: 'number',
            description: 'Sort order in menus (1, 2, 3, etc.)',
            initialValue: 1,
        }),
        defineField({
            name: 'description',
            title: 'Description',
            type: 'text',
            rows: 2,
        }),
    ],
    orderings: [
        {
            title: 'Display Order',
            name: 'orderAsc',
            by: [{ field: 'order', direction: 'asc' }],
        },
    ],
    preview: {
        select: {
            title: 'title',
            subtitle: 'slug.current',
        },
    },
})

