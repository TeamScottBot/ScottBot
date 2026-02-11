// export class OrderDO {
//   state: DurableObjectState
//   env: Env

//   constructor(state: DurableObjectState, env: Env) {
//     this.state = state
//     this.env = env
//   }

//   async fetch(req: Request) {
//     const url = new URL(req.url)

//     if (url.pathname === "/init") {
//       const data = await req.json()
//       await this.state.storage.put("order", {
//         status: "created",
//         ...data,
//       })
//       return new Response("ok")
//     }

//     if (url.pathname === "/update") {
//       const update = await req.json()
//       const order = await this.state.storage.get("order")
//       await this.state.storage.put("order", {
//         ...order,
//         ...update,
//       })
//       return new Response("ok")
//     }

//     if (url.pathname === "/finish") {
//       await this.state.storage.deleteAll()
//       return new Response("ok")
//     }

//     return new Response("not found", { status: 404 })
//   }
// }