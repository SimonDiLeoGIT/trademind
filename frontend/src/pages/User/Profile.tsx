import { useAuth0 } from "@auth0/auth0-react";
import { useEffect, useState } from "react";

const Profile = () => {
  
  const { user, isAuthenticated, isLoading, getAccessTokenSilently } = useAuth0();
  const [userMetadata, setUserMetadata] = useState(null);

  useEffect(() => {
    const getUserMetadata = async () => {
      const domain = import.meta.env.VITE_AUTH0_DOMAIN;

      try {
        const accessToken = await getAccessTokenSilently({
          authorizationParams: {
            audience: import.meta.env.VITE_AUTH0_AUDIENCE,
          },
        });

        console.log('accessToken', accessToken);
        console.log('user', user);
        // if (user) {

        //   const userDetailsByIdUrl = `https://${domain}/api/v2/users/${user.sub}`;
          
        //   const metadataResponse = await fetch(userDetailsByIdUrl, {
        //     headers: {
        //       Authorization: `Bearer ${accessToken}`,
        //     },
        //   });
        //   console.log(metadataResponse)
        //   const { user_metadata } = await metadataResponse.json();
          
        //   setUserMetadata(user_metadata);
        // }
      } catch (e: any) {
        console.log(e.message);
      }
    };

    getUserMetadata();
  }, [getAccessTokenSilently, user?.sub]);

  if (isLoading) {
    return <div>Loading ...</div>;
  }

  if (!isAuthenticated || !user) {
    return <div>Not authenticated</div>;
  }
  
  return (
    isAuthenticated && (
      <div>
        <img src={user.picture} alt={user.name} />
        <h2>{user.name}</h2>
        <p>{user.email}</p>
        <h3>User Metadata</h3>
        {userMetadata ? (
          <pre>{JSON.stringify(userMetadata, null, 2)}</pre>
        ) : (
          "No user metadata defined"
        )}
      </div>
    )
  );
};

export default Profile;