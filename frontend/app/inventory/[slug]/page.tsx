interface UserInventory {
    id: number;
    title: string;
    intro: string;
  }
  
  interface InventoryEntity {
    id: number;
    meta: {
      slug: string;
    };
    title: string;
    date: string;
    intro: string;
  }
  
  export default async function BlogIndex() {
    const indexPages = await fetch(
      `https://digidex.tech/api/v2/pages/?${new URLSearchParams({
        type: "inventory.UserInventory",
        slug: "inventory",
        fields: "intro",
      })}`,
      {
        headers: {
          Accept: "application/json",
        },
      }
    ).then((response) => response.json());
    // There's only one with the slug "inventory"
    const index: UserInventory = indexPages.items[0];
  
    // Fetch the InventoryEntity pages that are children of the UserInventory instance
    const data = await fetch(
      `https://digidex.tech/api/v2/pages/?${new URLSearchParams({
        type: "inventory.InventoryEntity",
        child_of: index.id.toString(),
        fields: ["date", "intro"].join(","),
      })}`,
      {
        headers: {
          Accept: "application/json",
        },
      }
    ).then((response) => response.json());
    // Use InventoryEntity instances as the posts
    const posts: InventoryEntity[] = data.items;
  
    return (
      <main>
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">{index.title}</h1>
          <div dangerouslySetInnerHTML={{ __html: index.intro }}></div>
        </div>
        {/* The rest is the same as the previous example */}
        <ul>
          {posts.map((child) => (
            <li key={child.id} className="mb-4">
              <a className="underline" href={`blog/${child.meta.slug}`}>
                <h2>{child.title}</h2>
              </a>
              <time dateTime={child.date}>
                {new Date(child.date).toDateString()}
              </time>
              <p>{child.intro}</p>
            </li>
          ))}
        </ul>
      </main>
    );
  }
  
  export async function generateStaticParams() {
    const data = await fetch(
      `https://digidex.tech/api/v2/pages/?${new URLSearchParams({
        type: "inventory.InventoryEntity",
      })}`,
      {
        headers: {
          Accept: "application/json",
        },
      }
    ).then((response) => response.json());
  
    return data.items.map((post: InventoryEntity) => ({
      slug: post.meta.slug,
    }));
  }