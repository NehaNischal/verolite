import { getCliClient } from 'sanity/cli'

async function testWrite() {
    try {
        const client = getCliClient()
        console.log("Client configured with project:", client.config().projectId)
        const doc = {
            _type: 'categoryGroup',
            _id: 'test-group-ping',
            title: 'Test Group Ping',
            slug: { _type: 'slug', current: 'test-group-ping' },
            order: 999
        }
        await client.createOrReplace(doc)
        console.log("SUCCESS: Created test-group-ping")
        await client.delete('test-group-ping')
        console.log("SUCCESS: Deleted test-group-ping")
    } catch (e) {
        console.error("WRITE TEST FAILED:", e)
    }
}

testWrite()

