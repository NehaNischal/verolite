import { getCliClient } from 'sanity/cli'

const PRIMARY_GROUPS = [
    {
        _id: 'categoryGroup-indoor',
        _type: 'categoryGroup',
        title: 'Indoor Lights',
        slug: { _type: 'slug', current: 'indoor' },
        order: 1,
        description: 'Architectural indoor lighting fixtures and systems'
    },
    {
        _id: 'categoryGroup-outdoor',
        _type: 'categoryGroup',
        title: 'Outdoor Lights',
        slug: { _type: 'slug', current: 'outdoor' },
        order: 2,
        description: 'Exterior and landscape architectural luminaires'
    },
    {
        _id: 'categoryGroup-drivers',
        _type: 'categoryGroup',
        title: 'Drivers & Controllers',
        slug: { _type: 'slug', current: 'drivers' },
        order: 3,
        description: 'LED drivers, dimmers, and intelligent sensor switches'
    },
    {
        _id: 'categoryGroup-emergency',
        _type: 'categoryGroup',
        title: 'Emergency Lights',
        slug: { _type: 'slug', current: 'emergency' },
        order: 4,
        description: 'Safety-critical LED emergency luminaires and exit signs'
    }
]

const SUBCATEGORIES = [
    // Indoor Lights
    {
        _id: 'category-recessed-led-down-lights',
        _type: 'category',
        title: 'Recessed LED Down Lights',
        slug: { _type: 'slug', current: 'recessed-led-down-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-indoor' },
        pageUrl: 'recessed-led-down-lights.html',
        order: 1
    },
    {
        _id: 'category-led-surface-down-lights',
        _type: 'category',
        title: 'LED Surface Down Lights',
        slug: { _type: 'slug', current: 'led-surface-down-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-indoor' },
        pageUrl: 'led-surface-down-lights.html',
        order: 2
    },
    {
        _id: 'category-3phase-track-lights',
        _type: 'category',
        title: '3-Phase Track Lights',
        slug: { _type: 'slug', current: '3phase-track-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-indoor' },
        pageUrl: '3phase-track-lights.html',
        order: 3
    },
    {
        _id: 'category-office-linear-lights',
        _type: 'category',
        title: 'Office Linear Lights',
        slug: { _type: 'slug', current: 'office-linear-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-indoor' },
        pageUrl: 'office-linear-lights.html',
        order: 4
    },
    {
        _id: 'category-led-strip-lights',
        _type: 'category',
        title: 'LED Strip Lights',
        slug: { _type: 'slug', current: 'led-strip-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-indoor' },
        pageUrl: 'led-strip-lights.html',
        order: 5
    },
    {
        _id: 'category-led-magnetic-track-lights',
        _type: 'category',
        title: 'LED Magnetic Track Lights',
        slug: { _type: 'slug', current: 'led-magnetic-track-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-indoor' },
        pageUrl: 'led-magnetic-track-lights.html',
        order: 6
    },

    // Outdoor Lights
    {
        _id: 'category-led-garden-lights',
        _type: 'category',
        title: 'LED Garden Lights',
        slug: { _type: 'slug', current: 'led-garden-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-outdoor' },
        pageUrl: 'led-garden-lights.html',
        order: 1
    },
    {
        _id: 'category-led-outdoor-flexible-neon-light',
        _type: 'category',
        title: 'LED Outdoor Flexible Neon Light',
        slug: { _type: 'slug', current: 'led-outdoor-flexible-neon-light' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-outdoor' },
        pageUrl: 'led-outdoor-flexible-neon-light.html',
        order: 2
    },

    // Drivers & Controllers
    {
        _id: 'category-led-strip-light-drivers',
        _type: 'category',
        title: 'LED Strip Light Drivers',
        slug: { _type: 'slug', current: 'led-strip-light-drivers' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-drivers' },
        pageUrl: 'led-strip-light-drivers.html',
        order: 1
    },
    {
        _id: 'category-led-phase-cut-dimmer',
        _type: 'category',
        title: 'LED Phase Cut Dimmer',
        slug: { _type: 'slug', current: 'led-phase-cut-dimmer' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-drivers' },
        pageUrl: 'led-phase-cut-dimmer.html',
        order: 2
    },
    {
        _id: 'category-led-sensor-switches',
        _type: 'category',
        title: 'LED Sensor Switches',
        slug: { _type: 'slug', current: 'led-sensor-switches' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-drivers' },
        pageUrl: 'led-sensor-switches.html',
        order: 3
    },

    // Emergency Lights
    {
        _id: 'category-emergency-lights',
        _type: 'category',
        title: 'Emergency Lights',
        slug: { _type: 'slug', current: 'emergency-lights' },
        parentGroup: { _type: 'reference', _ref: 'categoryGroup-emergency' },
        pageUrl: 'emergency-lights.html',
        order: 1
    }
]

async function seedAndMigrate() {
    const client = getCliClient()
    console.log("Seeding primary category groups...")
    for (const group of PRIMARY_GROUPS) {
        await client.createOrReplace(group)
        console.log(`  [Group Created/Updated]: ${group.title} (${group._id})`)
    }

    console.log("\nSeeding subcategories...")
    for (const subcat of SUBCATEGORIES) {
        await client.createOrReplace(subcat)
        console.log(`  [Subcategory Created/Updated]: ${subcat.title} (${subcat._id})`)
    }

    console.log("\nMigrating existing products to use category references...")
    const products = await client.fetch<Array<{ _id: string, name: string, category: any }>>('*[_type == "product"]')
    console.log(`Found ${products.length} products to verify/migrate.`)

    let migrated = 0
    for (const prod of products) {
        // If category is a string (e.g. 'recessed-led-down-lights')
        if (typeof prod.category === 'string') {
            const catId = `category-${prod.category}`
            await client.patch(prod._id)
                .set({
                    category: {
                        _type: 'reference',
                        _ref: catId
                    },
                    categorySlug: prod.category
                })
                .commit()
            console.log(`  Migrated product "${prod.name}" -> ${catId}`)
            migrated++
        }
    }

    console.log(`\nSuccessfully migrated ${migrated} products to category references!`)
}

seedAndMigrate().catch(err => {
    console.error("Migration failed:", err)
    process.exit(1)
})

