import { getCliClient } from 'sanity/cli'
import * as fs from 'fs'
import * as path from 'path'

async function seedEmergencyProduct() {
    const client = getCliClient()
    const imgPath = path.resolve(__dirname, '../../images/emergency-hero-banner.jpg')

    let imageAsset: any = null
    if (fs.existsSync(imgPath)) {
        console.log("Uploading emergency exit sign image...")
        imageAsset = await client.assets.upload('image', fs.createReadStream(imgPath), {
            filename: 'emergency-exit-sign.jpg',
        })
        console.log("Uploaded image asset:", imageAsset._id)
    }

    const doc: any = {
        _id: 'product-emergency-exit-sign',
        _type: 'product',
        name: 'Emergency Exit Sign',
        model: 'VER-EMG-01',
        slug: { _type: 'slug', current: 'emergency-exit-sign' },
        category: {
            _type: 'reference',
            _ref: 'category-emergency-lights'
        },
        categorySlug: 'emergency-lights',
        shortDescription: 'Architectural LED emergency exit sign with long-life LiFePO4 battery backup, crisp laser-etched green pictogram panels, and ISO 7010 compliance.',
        description: 'Engineered specifically for safety-critical architectural and commercial environments, the VEROLITE Emergency Exit Sign delivers instant, dependable illumination during emergency power failures. Constructed with a precision anodised aluminium housing and crystal-clear high-efficiency optical acrylic diffuser, it ensures maximum visibility and legibility up to 24 metres. Fully certified to BS EN 60598-2-22, BS 5266-1, and ISO 7010 international standards.',
        features: [
            'Ultra-reliable high-efficiency LED light source with 50,000+ hour operational lifespan',
            'Maintained and non-maintained operation modes selectable via onboard DIP switch',
            'Integrated 3-hour emergency battery backup with self-testing diagnostics',
            'Surface wall, ceiling, or semi-recessed mounting options included',
            'ISO 7010 and BS EN 1838 compliant optical pictogram panel (Running Man with Arrow)',
            'Robust IP42 rated aluminium architectural body with anti-corrosion finish'
        ],
        specifications: [
            { label: 'Type', value: 'Architectural LED Emergency Exit Luminaire' },
            { label: 'Emergency Duration', value: '3 Hours' },
            { label: 'Mode of Operation', value: 'Maintained / Non-Maintained Selectable' },
            { label: 'Input Voltage', value: 'AC 220-240V, 50/60Hz' },
            { label: 'Battery Type', value: 'LiFePO4 3.2V 1500mAh High Temperature' },
            { label: 'Viewing Distance', value: '24 Metres (ISO 7010)' },
            { label: 'Housing Material', value: 'Anodised Aluminium + Optical Grade Acrylic' },
            { label: 'IP Rating', value: 'IP42' },
            { label: 'Compliance Standards', value: 'BS EN 60598-2-22, BS 5266-1, ISO 7010' }
        ],
        variantHeaders: {
            col1: 'Model',
            col2: 'Wattage',
            col3: 'Direction',
            col4: 'Finish',
            col5: 'Mounting',
            col6: 'Emergency Duration'
        },
        variants: [
            { model: 'VER-EMG-01-D', wattage: '3W', cct: 'Arrow Down (Exit)', body: 'Silver Anodised Aluminium', size: 'Wall / Ceiling Surface', cutOut: '3 Hours LiFePO4' },
            { model: 'VER-EMG-01-L', wattage: '3W', cct: 'Arrow Left', body: 'Silver Anodised Aluminium', size: 'Wall / Ceiling Surface', cutOut: '3 Hours LiFePO4' },
            { model: 'VER-EMG-01-R', wattage: '3W', cct: 'Arrow Right', body: 'Silver Anodised Aluminium', size: 'Wall / Ceiling Surface', cutOut: '3 Hours LiFePO4' }
        ],
        seoTitle: 'Emergency Exit Sign (VER-EMG-01) | VEROLITE Architectural Lighting',
        seoDescription: 'Discover the Emergency Exit Sign luminaire by VEROLITE. Code-compliant architectural emergency lighting with 3-hour battery backup and ISO 7010 pictograms.'
    }

    if (imageAsset) {
        doc.mainImage = {
            _type: 'image',
            asset: {
                _type: 'reference',
                _ref: imageAsset._id
            }
        }
    }

    await client.createOrReplace(doc)
    console.log("SUCCESS: Created product-emergency-exit-sign in Sanity dataset!")
}

seedEmergencyProduct().catch(e => {
    console.error("Error seeding emergency product:", e)
    process.exit(1)
})

