import React from 'react';
import { WalletConnectSection } from './Interaction'; // Check your export names!
import { SolanaFraudStatusChecker } from './ScoreDisplay'; // Check export names!
import { SolanaProviderWrapper } from './WalletWrapper'; // Check export names!
export { default as App } from './app.jsx';
import './app.css';

// Ensure you import the CSS for the wallet adapter
import '@solana/wallet-adapter-react-ui/styles.css';

function App() {
  return (
    <SolanaProviderWrapper>
      <div className="App">
        <h1>Sentinel Ledger</h1>
        <WalletConnectSection />
        {/* You need to pass a transaction ID here or standard input */}
        <SolanaFraudStatusChecker transactionId="YOUR_TEST_TX_ID" />
      </div>
    </SolanaProviderWrapper>
  );
}

export default App;
import ReactDOM from "react-dom/client";

ReactDOM.createRoot(document.getElementById("root")).render(<App />);