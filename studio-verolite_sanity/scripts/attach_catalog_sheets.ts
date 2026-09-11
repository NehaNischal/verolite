import { createClient } from '@sanity/client'
import * as fs from 'fs'
import * as path from 'path'

const token = 'skuJynYqVmI9aQjZxG313grBUNB9FuiDzli1SeoIhljIWiou6uNxTdyLguB8WqbPGaX5lffGR3zqV0vyab6DmWq3ZRDTNEZ9UI7lu5jr95902Gz5s30RaIZqoW5RrQCWCOo6ZDjQSHpHtaKujh4MdTl6hqgmzI3l3B75RVFkm3bQT1gbmQLq'

const client = createClient({
  projectId: '5nckxq6b',
  dataset: 'production',
  apiVersion: '2023-08-01',
  useCdn: false,
  token: token,
})

const sheetsDir = path.resolve(__dirname, '..', '..', 'catalog_sheets')

async function updateGalleries() {
  console.log('Connecting to Sanity and fetching products...')
  const products = await client.fetch('*[_type == "product"]{ _id, name, "slug": slug.current, mainImage }')
  console.log(`Found ${products.length} products to update with catalog sheets.`)

  let updated = 0
  for (const prod of products) {
    if (!prod.slug) continue
    const sheetFilename = `${prod.slug}-sheet.jpg`
    const sheetPath = path.join(sheetsDir, sheetFilename)

    if (fs.existsSync(sheetPath)) {
      try {
        console.log(`Uploading catalog sheet for ${prod.name} (${prod.slug})...`)
        const stream = fs.createReadStream(sheetPath)
        const asset = await client.assets.upload('image', stream, {
          filename: sheetFilename,
        })

        // Add main image and sheet image to gallery array
        const galleryItems: any[] = []
        if (prod.mainImage) {
          galleryItems.push(prod.mainImage)
        }
        galleryItems.push({
          _key: `sheet-${prod.slug}`,
          _type: 'image',
          asset: {
            _type: 'reference',
            _ref: asset._id,
          },
        })

        await client
          .patch(prod._id)
          .set({ gallery: galleryItems })
          .commit()

        console.log(`[SUCCESS] Attached datasheet gallery to ${prod.name}`)
        updated++
      } catch (err) {
        console.error(`[ERROR] Failed to attach sheet for ${prod.name}:`, err)
      }
    } else {
      console.warn(`[MISSING] No sheet found for ${prod.slug} at ${sheetPath}`)
    }
  }

  console.log(`\nSuccessfully updated ${updated} products with interactive datasheet galleries in Sanity!`)
}

updateGalleries().catch(console.error)
