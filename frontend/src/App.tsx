// import React from 'react';
import './App.css';
import { Amplify } from 'aws-amplify';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

const App: React.FC = () => {
  Amplify.configure({
    Auth: {
      userPoolId: import.meta.env.VITE_APP_USER_POOL_ID,
      userPoolWebClientId: import.meta.env.VITE_APP_USER_POOL_CLIENT_ID,
      authenticationFlowType: "USER_SRP_AUTH",
    },
  });
  return (
    <Authenticator
      components={{
        Header: () => (
          <div className="mb-5 mt-10 flex justify-center text-3xl text-aws-font-color">
            Bedrock Claude Chat
          </div>
        ),
      }}
    >
      {({ signOut, user }) => (
        <div className="relative flex h-screen w-screen bg-aws-paper">
          <header className="App-header">
            <h1>Hello {user?.username}</h1>
            <button onClick={signOut}>Sign out</button>
          </header>
        </div>
      )}
    </Authenticator>
  );
}

export default App;
