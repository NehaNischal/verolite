import { defineField, defineType } from 'sanity'

export const category = defineType({
    name: 'category',
    title: 'Subcategory',
    type: 'document',
    fields: [
        defineField({
            name: 'title',
            title: 'Subcategory Name',
            type: 'string',
            description: 'Subcategory title (e.g. Emergency Lights, Recessed LED Down Lights, LED Garden Lights)',
            validation: (Rule) => Rule.required(),
        }),
        defineField({
            name: 'slug',
            title: 'Slug',
            type: 'slug',
            description: 'Matches the website page slug (e.g. emergency-lights, recessed-led-down-lights)',
            options: {
                source: 'title',
                maxLength: 96,
            },
            validation: (Rule) => Rule.required(),
        }),
        defineField({
            name: 'parentGroup',
            title: 'Primary Category (Parent Group)',
            type: 'reference',
            to: [{ type: 'categoryGroup' }],
            description: 'Select the primary website category this belongs to (Indoor Lights, Outdoor Lights, Drivers & Controllers, Emergency Lights)',
            validation: (Rule) => Rule.required(),
        }),
        defineField({
            name: 'pageUrl',
            title: 'Website Page URL',
            type: 'string',
            description: 'Optional website page file (e.g. emergency-lights.html, recessed-led-down-lights.html)',
        }),
        defineField({
            name: 'order',
            title: 'Display Order',
            type: 'number',
            description: 'Sort order within its parent group',
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
            parentTitle: 'parentGroup.title',
            slug: 'slug.current',
        },
        prepare({ title, parentTitle, slug }) {
            return {
                title: title || 'Untitled Subcategory',
                subtitle: parentTitle ? `[${parentTitle}] /${slug || ''}` : `/${slug || ''}`,
            }
        },
    },
})

