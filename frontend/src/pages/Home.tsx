import { useAuth0 } from "@auth0/auth0-react";

const Home = () => {

  const { loginWithRedirect } = useAuth0();

  return (
    <main>
      <h1>Trade Mind</h1>
      <section>
        <button onClick={() => loginWithRedirect()}>Log In</button>
      </section>
    </main>
  )
}

export default Home