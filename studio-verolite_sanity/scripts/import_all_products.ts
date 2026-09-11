import { getCliClient } from 'sanity/cli'
import * as fs from 'fs'
import * as path from 'path'

// Category display mapping
const CATEGORY_DETAILS: Record<string, { title: string, defaultSpecs: { label: string, value: string }[], features: string[] }> = {
  'recessed-led-down-lights': {
    title: 'Recessed LED Down Light',
    defaultSpecs: [
      { label: 'Type', value: 'Recessed Architectural Downlight' },
      { label: 'CRI', value: 'Ra > 90 / 95' },
      { label: 'CCT', value: '2700K / 3000K / 4000K' },
      { label: 'Material', value: 'Die-cast Aluminum Housing' },
      { label: 'IP Rating', value: 'IP20 / IP44' },
      { label: 'Dimming Support', value: 'TRIAC / 0-10V / DALI' }
    ],
    features: [
      'Deep anti-glare reflector design (UGR < 19)',
      'High color rendering Ra > 90 for true color fidelity',
      'Superior thermal dissipation with die-cast aluminum heat sink',
      'Tool-free fast spring mounting system'
    ]
  },
  'led-surface-down-lights': {
    title: 'LED Surface Down Light',
    defaultSpecs: [
      { label: 'Type', value: 'Surface-Mounted Ceiling Downlight' },
      { label: 'CRI', value: 'Ra > 90' },
      { label: 'CCT', value: '3000K / 4000K / 6000K' },
      { label: 'Housing Finish', value: 'Matt White / Matt Black' },
      { label: 'Input Voltage', value: 'AC 220-240V, 50/60Hz' },
      { label: 'IP Rating', value: 'IP20' }
    ],
    features: [
      'Sleek surface-mounted cylinder / square profile',
      'Clean ceiling aesthetic without requiring cut-out apertures',
      'Uniform diffused optical illumination',
      'Integrated driver for direct mains connection'
    ]
  },
  '3phase-track-lights': {
    title: '3-Phase Track Light',
    defaultSpecs: [
      { label: 'Track System', value: 'Universal 3-Phase 4-Wire Global Track' },
      { label: 'Rotation', value: '350° Horizontal, 90° Vertical' },
      { label: 'CRI', value: 'Ra > 92' },
      { label: 'Beam Angle', value: '15° / 24° / 36° interchangeable' },
      { label: 'Housing', value: 'Aviation Aluminum' }
    ],
    features: [
      '350-degree horizontal swivel and 90-degree vertical tilt',
      'Interchangeable precision optical lenses',
      'Compatible with standard 3-phase European track profiles',
      'High lumen output with low glare honeycomb louver accessory'
    ]
  },
  'led-garden-lights': {
    title: 'LED Garden & Landscape Light',
    defaultSpecs: [
      { label: 'IP Rating', value: 'IP65 / IP67 Waterproof' },
      { label: 'Housing', value: 'Die-cast Aluminum + Anti-corrosion Powder Coat' },
      { label: 'CCT', value: '3000K Warm White / Amber / RGBW' },
      { label: 'Input Voltage', value: 'AC 100-240V / DC 24V' },
      { label: 'Impact Rating', value: 'IK08' }
    ],
    features: [
      'IP65/IP67 rated waterproof enclosure for all-weather outdoor environments',
      'Anti-corrosion powder coating resistant to UV and coastal conditions',
      'Precision ground spike or surface base mounting',
      'Optimized beam distribution for trees, pathways, and architectural facades'
    ]
  },
  'led-strip-lights': {
    title: 'LED Strip Light',
    defaultSpecs: [
      { label: 'Voltage', value: 'DC 24V Constant Voltage' },
      { label: 'CRI', value: 'Ra > 90 / Ra > 95' },
      { label: 'LED Density', value: 'COB Seamless / 120-240 LEDs/m' },
      { label: 'PCB Width', value: '8mm / 10mm Dual-layer Copper' },
      { label: 'Cut Interval', value: 'Every 25mm / 50mm' }
    ],
    features: [
      'Dot-free seamless linear illumination (COB technology)',
      'High thermal conductivity dual-layer 2oz/3oz pure copper PCB',
      'Accurate 3-step MacAdam ellipse color consistency',
      'Industrial grade 3M adhesive backing for durable thermal bonding'
    ]
  },
  'led-outdoor-flexible-neon-light': {
    title: 'LED Outdoor Flexible Neon Light',
    defaultSpecs: [
      { label: 'Material', value: 'Food-grade Silicone Extrusion' },
      { label: 'IP Rating', value: 'IP67 / IP68 Submersible / Outdoor' },
      { label: 'Bending Direction', value: 'Top-bending / Side-bending 3D Flex' },
      { label: 'Voltage', value: 'DC 24V' },
      { label: 'UV Resistance', value: 'Saltwater & UV Resistant' }
    ],
    features: [
      '100% silicone extrusion resistant to UV, yellowing, chlorine, and saltwater',
      'Completely dot-free diffused uniform neon glow',
      'Extreme flexibility for organic curved architectural lines and coves',
      'IP67 injection molded end-caps with waterproof cable entries'
    ]
  },
  'led-magnetic-track-lights': {
    title: 'LED Magnetic Track Light System',
    defaultSpecs: [
      { label: 'System Voltage', value: 'DC 48V Safe Extra-Low Voltage (SELV)' },
      { label: 'Mounting Style', value: 'Recessed / Surface / Pendant Magnetic Profile' },
      { label: 'Control', value: 'ON/OFF, DALI 2.0, Tuya Zigbee, 0-10V' },
      { label: 'Finish', value: 'Anodized Architectural Black / White' }
    ],
    features: [
      'Tool-free snap-in magnetic mechanical locking mechanism',
      'Safe 48V low voltage touch-safe track busbars',
      'Modular interchangeability between linear, spotlight, and pendant modules',
      'Seamless corner connectors and ultra-slim recessed trimless options'
    ]
  },
  'office-linear-lights': {
    title: 'Office Linear Light',
    defaultSpecs: [
      { label: 'Mounting', value: 'Suspended Pendant / Surface / Recessed' },
      { label: 'UGR Rating', value: 'UGR < 19 Office Glare Compliant' },
      { label: 'Optical System', value: 'Micro-prismatic Diffuser / Louver Reflector' },
      { label: 'CCT', value: '3000K / 4000K / 5000K Tunable White' },
      { label: 'Efficacy', value: 'Up to 130 lm/W' }
    ],
    features: [
      'Low-glare microprismatic optics designed for computer screen workstations',
      'Direct / Indirect (Up/Down) bidirectional illumination options',
      'Seamless continuous linking for long run architectural spans',
      'Integrated DALI or 0-10V intelligent dimming controls'
    ]
  },
  'led-strip-light-drivers': {
    title: 'LED Strip Light Driver / Power Supply',
    defaultSpecs: [
      { label: 'Output Voltage', value: 'DC 12V / 24V Constant Voltage' },
      { label: 'Efficiency', value: '> 90%' },
      { label: 'Power Factor', value: 'PF > 0.95 Active PFC' },
      { label: 'Protection', value: 'Short Circuit / Overload / Over Temperature' },
      { label: 'Warranty', value: '5-Year Commercial Warranty' }
    ],
    features: [
      'Ultra-quiet flicker-free performance across the full dimming range',
      'Built-in active PFC with high efficiency thermal aluminum case',
      'Full suite of protections (auto-recovery short circuit, over-voltage, over-temp)',
      'Available in IP20 slim indoor and IP65/IP67 rugged outdoor configurations'
    ]
  },
  'led-phase-cut-dimmer': {
    title: 'LED Phase Cut Dimmer',
    defaultSpecs: [
      { label: 'Dimming Mode', value: 'Trailing Edge (Reverse Phase) / Leading Edge' },
      { label: 'Load Range', value: '5W - 300W LED Load' },
      { label: 'Input Voltage', value: 'AC 220-240V 50Hz' },
      { label: 'Compatibility', value: 'Standard EU / UK Wall Box Mounting' }
    ],
    features: [
      'Smooth 0-100% stepless dimming without buzzing or flickering',
      'Configurable minimum brightness trim potentiometer',
      'Trailing-edge MOSFET technology optimized for modern dimmable LED loads',
      'Soft start technology to extend LED luminaire lifespan'
    ]
  },
  'led-sensor-switches': {
    title: 'LED Sensor Switch & Controller',
    defaultSpecs: [
      { label: 'Sensor Type', value: 'Infrared / Microwave Motion / Door Trigger / Touch' },
      { label: 'Operating Voltage', value: 'DC 12V - 24V / AC 220V' },
      { label: 'Detection Range', value: '1m - 8m (Adjustable)' },
      { label: 'Time Delay', value: '5s - 10min Configurable' }
    ],
    features: [
      'High-sensitivity detection for automated cabinetry, wardrobes, and hallways',
      'Compact low-profile form factor for discreet concealment in joinery',
      'Instant trigger response with silent electronic solid-state switching',
      'Energy saving automatic shut-off when no presence is detected'
    ]
  }
}

// 47 products dataset
const STATIC_PRODUCTS = [
  // Recessed LED Down Lights (16)
  { category: 'recessed-led-down-lights', name: 'VERO OLIV', model: 'VERO OLIV', slug: 'vero-oliv', image: 'images/recessed/oliv.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO NIKO', model: 'VERO NIKO', slug: 'vero-niko', image: 'images/recessed/niko.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO RAZA', model: 'VERO RAZA', slug: 'vero-raza', image: 'images/recessed/raza.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO KIA', model: 'VERO KIA', slug: 'vero-kia', image: 'images/recessed/kia.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO LUXA', model: 'VERO LUXA', slug: 'vero-luxa', image: 'images/recessed/luxa.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO VEXO', model: 'VERO VEXO', slug: 'vero-vexo', image: 'images/recessed/vexo.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO TALON', model: 'VERO TALON', slug: 'vero-talon', image: 'images/recessed/talon.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO ORBIT', model: 'VERO ORBIT', slug: 'vero-orbit', image: 'images/recessed/orbit.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO ORBIT-S', model: 'VERO ORBIT-S', slug: 'vero-orbit-s', image: 'images/recessed/orbit-s.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO ORBIT-2', model: 'VERO ORBIT-2', slug: 'vero-orbit-2', image: 'images/recessed/orbit-2.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO ORBIT-3', model: 'VERO ORBIT-3', slug: 'vero-orbit-3', image: 'images/recessed/orbit-3.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO TERA', model: 'VERO TERA', slug: 'vero-tera', image: 'images/recessed/tera.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO SYRO', model: 'VERO SYRO', slug: 'vero-syro', image: 'images/recessed/syro.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO RIVO R', model: 'VERO RIVO R', slug: 'vero-rivo-r', image: 'images/recessed/rivo-r.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO RIVO S', model: 'VERO RIVO S', slug: 'vero-rivo-s', image: 'images/recessed/rivo-s.jpg' },
  { category: 'recessed-led-down-lights', name: 'VERO RIVO 2', model: 'VERO RIVO 2', slug: 'vero-rivo-2', image: 'images/recessed/rivo-2.jpg' },

  // LED Surface Down Lights (5)
  { category: 'led-surface-down-lights', name: 'VERO DAXO', model: 'VERO DAXO', slug: 'vero-daxo', image: 'images/surface/daxo.jpg' },
  { category: 'led-surface-down-lights', name: 'VERO ZIVON', model: 'VERO ZIVON', slug: 'vero-zivon', image: 'images/surface/zivon.jpg' },
  { category: 'led-surface-down-lights', name: 'VERO ARCO-7', model: 'VERO ARCO-7', slug: 'vero-arco-7', image: 'images/surface/arco-7.jpg' },
  { category: 'led-surface-down-lights', name: 'VERO ARCO-8', model: 'VERO ARCO-8', slug: 'vero-arco-8', image: 'images/surface/arco-8.jpg' },
  { category: 'led-surface-down-lights', name: 'VERO NOVA', model: 'VERO NOVA', slug: 'vero-nova', image: 'images/surface/nova.jpg' },

  // 3-Phase Track Lights (1)
  { category: '3phase-track-lights', name: 'VERO LYNX', model: 'VERO LYNX', slug: 'vero-lynx', image: 'images/track/lynx.jpg' },

  // LED Garden Lights (2)
  { category: 'led-garden-lights', name: 'VERO HELI', model: 'VERO HELI', slug: 'vero-heli', image: 'images/outdoor/heli.jpg' },
  { category: 'led-garden-lights', name: 'VERO ZION', model: 'VERO ZION', slug: 'vero-zion', image: 'images/outdoor/zion.jpg' },

  // LED Strip Lights (3)
  { category: 'led-strip-lights', name: 'VERO NEXO', model: 'VERO NEXO', slug: 'vero-nexo', image: 'images/strip/nexo.jpg' },
  { category: 'led-strip-lights', name: 'VERO NEXO-COB', model: 'VERO NEXO-COB', slug: 'vero-nexo-cob', image: 'images/strip/nexo-cob.jpg' },
  { category: 'led-strip-lights', name: 'VERO NEXO-IP65', model: 'VERO NEXO-IP65', slug: 'vero-nexo-ip65', image: 'images/strip/nexo-ip65.jpg' },

  // LED Outdoor Flexible Neon Light (1)
  { category: 'led-outdoor-flexible-neon-light', name: 'VERO REO NEON', model: 'VERO REO NEON', slug: 'vero-reo-neon', image: 'images/outdoor/reo.jpg' },

  // LED Magnetic Track Lights (6)
  { category: 'led-magnetic-track-lights', name: 'VERO MAGNETIC TRACK CHANNEL', model: 'VERO CHANNEL', slug: 'vero-magnetic-track-channel', image: 'images/magnetic/channel.jpg' },
  { category: 'led-magnetic-track-lights', name: 'VERO XENON', model: 'VERO XENON', slug: 'vero-xenon', image: 'images/magnetic/xenon.jpg' },
  { category: 'led-magnetic-track-lights', name: 'VERO LINAN', model: 'VERO LINAN', slug: 'vero-linan', image: 'images/magnetic/linan.jpg' },
  { category: 'led-magnetic-track-lights', name: 'VERO TITAN', model: 'VERO TITAN', slug: 'vero-titan', image: 'images/magnetic/titan.jpg' },
  { category: 'led-magnetic-track-lights', name: 'VERO VEGA', model: 'VERO VEGA', slug: 'vero-vega', image: 'images/magnetic/vega.jpg' },
  { category: 'led-magnetic-track-lights', name: 'VERO AERO', model: 'VERO AERO', slug: 'vero-aero', image: 'images/magnetic/aero.jpg' },

  // Office Linear Lights (3)
  { category: 'office-linear-lights', name: 'VERO LINO', model: 'VERO LINO', slug: 'vero-lino', image: 'images/office/lino.jpg' },
  { category: 'office-linear-lights', name: 'VERO REO LINEAR', model: 'VERO REO LINEAR', slug: 'vero-reo-linear', image: 'images/office/reo.jpg' },
  { category: 'office-linear-lights', name: 'VERO RECTA', model: 'VERO RECTA', slug: 'vero-recta', image: 'images/office/recta.jpg' },

  // LED Strip Light Drivers (5)
  { category: 'led-strip-light-drivers', name: 'VERO DRIVER IP20', model: 'VERO DRIVER IP20', slug: 'vero-driver-ip20', image: 'images/drivers/driver-ip20.jpg' },
  { category: 'led-strip-light-drivers', name: 'VERO DRIVER IP65', model: 'VERO DRIVER IP65', slug: 'vero-driver-ip65', image: 'images/drivers/driver-ip65.jpg' },
  { category: 'led-strip-light-drivers', name: 'VERO DIMMING DRIVER IP65', model: 'VERO DIMMING DRIVER IP65', slug: 'vero-dimming-driver-ip65', image: 'images/drivers/constant-voltage-dimming-ip65.jpg' },
  { category: 'led-strip-light-drivers', name: 'VERO DIMMING DRIVER IP20', model: 'VERO DIMMING DRIVER IP20', slug: 'vero-dimming-driver-ip20', image: 'images/drivers/constant-voltage-dimming-ip20.jpg' },
  { category: 'led-strip-light-drivers', name: 'VERO CONSTANT CURRENT DIMMING', model: 'VERO CC DIMMING', slug: 'vero-constant-current-dimming', image: 'images/drivers/constant-current-dimming.jpg' },

  // LED Phase Cut Dimmer (1)
  { category: 'led-phase-cut-dimmer', name: 'VERO PHASE CUT DIMMER', model: 'VERO PHASE CUT DIMMER', slug: 'vero-phase-cut-dimmer', image: 'images/dimmer/phase-cut-dimmer.jpg' },

  // LED Sensor Switches (4)
  { category: 'led-sensor-switches', name: 'VERO CABINET DOOR SENSOR', model: 'VERO CABINET SENSOR', slug: 'vero-cabinet-door-sensor', image: 'images/sensors/cabinet-door-sensor.jpg' },
  { category: 'led-sensor-switches', name: 'VERO WIRELESS MOTION SENSOR', model: 'VERO WIRELESS PIR', slug: 'vero-wireless-motion-sensor', image: 'images/sensors/wireless-motion-sensor.jpg' },
  { category: 'led-sensor-switches', name: 'VERO WIRELESS DOOR SENSOR', model: 'VERO WIRELESS DOOR', slug: 'vero-wireless-door-sensor', image: 'images/sensors/wireless-door-sensor.jpg' },
  { category: 'led-sensor-switches', name: 'VERO PARTITION TOUCH & HAND WAVE', model: 'VERO TOUCH & HANDWAVE', slug: 'vero-partition-touch-hand-wave', image: 'images/sensors/partition-touch-handwave-sensor.jpg' },
]

import { createClient } from '@sanity/client'

async function importAll() {
  const token = process.env.SANITY_AUTH_TOKEN || process.env.SANITY_TOKEN || process.argv[2]
  const client = createClient({
    projectId: '5nckxq6b',
    dataset: 'production',
    apiVersion: '2023-08-01',
    useCdn: false,
    token: token || undefined,
  })
  console.log(`Starting import of ${STATIC_PRODUCTS.length} static products into Sanity CMS (project: 5nckxq6b)...`)
  if (!token) {
    console.warn(`[WARNING] No SANITY_AUTH_TOKEN provided. If write permissions are restricted, provide a Write token.`)
  }

  // Cache uploaded images to avoid re-uploading duplicate paths
  const uploadedImageMap: Record<string, string> = {}

  let createdCount = 0
  let updatedCount = 0

  for (const item of STATIC_PRODUCTS) {
    const config = CATEGORY_DETAILS[item.category] || {
      title: 'Architectural Lighting',
      defaultSpecs: [{ label: 'Brand', value: 'VEROLITE' }],
      features: ['Premium architectural illumination', 'High efficiency engineering']
    }

    // Resolve local image path
    const cleanImgPath = item.image.split('?')[0].replace('/', path.sep)
    const localImagePath = path.resolve(__dirname, '..', '..', cleanImgPath)

    let imageAssetId = uploadedImageMap[localImagePath]

    if (!imageAssetId && fs.existsSync(localImagePath)) {
      try {
        console.log(`Uploading image for ${item.name}: ${cleanImgPath}`)
        const imageStream = fs.createReadStream(localImagePath)
        const asset = await client.assets.upload('image', imageStream, {
          filename: path.basename(localImagePath),
        })
        imageAssetId = asset._id
        uploadedImageMap[localImagePath] = asset._id
      } catch (err) {
        console.warn(`Failed to upload image for ${item.name}:`, err)
      }
    }

    const docId = `product-${item.slug}`

    const docData: any = {
      _id: docId,
      _type: 'product',
      name: item.name,
      model: item.model,
      slug: {
        _type: 'slug',
        current: item.slug,
      },
      category: item.category,
      shortDescription: `Verolite ${item.name} is a high-performance ${config.title.toLowerCase()} engineered for modern luxury residential, hospitality, and commercial architecture.`,
      description: `The ${item.name} series exemplifies Verolite's commitment to precision optics, understated elegance, and dependable performance. Crafted from premium materials with sophisticated thermal management, it delivers clean, glare-free illumination that elevates contemporary interior and exterior spaces.`,
      features: config.features,
      specifications: config.defaultSpecs.map((s, idx) => ({
        _key: `spec-${idx + 1}`,
        label: s.label,
        value: s.value
      })),
      variants: [
        {
          _key: `variant-1`,
          model: item.model,
          wattage: 'Standard',
          cct: '3000K / 4000K',
          body: 'Architectural Finish',
          size: 'Standard',
          cutOut: 'Standard'
        }
      ]
    }

    if (imageAssetId) {
      docData.mainImage = {
        _type: 'image',
        asset: {
          _type: 'reference',
          _ref: imageAssetId,
        },
      }
    }

    try {
      await client.createOrReplace(docData)
      console.log(`[SUCCESS] Imported: ${item.name} (${item.slug}) -> Category: ${item.category}`)
      createdCount++
    } catch (err) {
      console.error(`[ERROR] Failed to create document for ${item.name}:`, err)
    }
  }

  console.log(`\n========================================`)
  console.log(`Import finished! Successfully imported ${createdCount} / ${STATIC_PRODUCTS.length} products to Sanity CMS.`)
  console.log(`========================================`)
}

importAll().catch((err) => {
  console.error('Fatal error in import script:', err)
  process.exit(1)
})
