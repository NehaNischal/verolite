import { getCliClient } from 'sanity/cli'

async function main() {
  const client = getCliClient()
  const dataset = client.config().dataset
  const projectId = client.config().projectId
  console.log(`Connected to Sanity: project=${projectId}, dataset=${dataset}`)
  
  const existingProducts = await client.fetch('*[_type == "product"]{_id, name, "slug": slug.current}')
  console.log(`Found ${existingProducts.length} existing products in Sanity:`, existingProducts)
}

main().catch((err) => {
  console.error('Error running test:', err)
  process.exit(1)
})
