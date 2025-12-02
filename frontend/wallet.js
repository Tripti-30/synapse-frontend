
JAVASCRIPT
import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react';
import { WalletModalProvider, WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import { clusterApiUrl } from '@solana/web3.js';
import { WalletAdapterNetwork } from '@solana/wallet-adapter-base';
import { useMemo } from 'react';
export function checkBalance(){
    console.log("Balance checked");
}


// Import the CSS for the UI components
import '@solana/wallet-adapter-react-ui/styles.css'; 

function SolanaProviderWrapper({ children }) {
    // Choose your network: devnet, testnet, or mainnet-beta
    const network = WalletAdapterNetwork.Devnet;
    const endpoint = useMemo(() => clusterApiUrl(network), [network]);

    // Define the wallets your app supports (Phantom, Solflare, etc.)
    const wallets = useMemo(
        () => [
            // Add specific wallet adapters here
            // e.g., getPhantomWallet(), getSolflareWallet(), etc.
        ],
        [network]
    );

    return (
        <ConnectionProvider endpoint={endpoint}>
            <WalletProvider wallets={wallets} autoConnect>
                <WalletModalProvider>
                    {children}
                </WalletModalProvider>
            </WalletProvider>
        </ConnectionProvider>
    );
}

// Wrap your main App component with this: <SolanaProviderWrapper><App /></SolanaProviderWrapper>
