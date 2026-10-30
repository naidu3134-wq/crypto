import streamlit as st
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

st.set_page_config(
    page_title="HTTP vs TLS Interception Lab",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Unsecured HTTP Interception vs. TLS Protection")
st.markdown("Demonstration of packet sniffing vulnerabilities and cryptographic mitigation using TLS.")


st.sidebar.header("Network Protocol Settings")
protocol = st.sidebar.radio(
    "Select Transmission Protocol:",
    ("Plain HTTP (Unsecured - Port 8080)", "HTTPS / TLS 1.3 (Encrypted - Port 8443)")
)

st.sidebar.markdown("---")
st.sidebar.subheader("Protocol Metadata")
if "HTTP" in protocol and "Plain" in protocol:
    st.sidebar.error("❌ TLS: Disabled")
    st.sidebar.warning("⚠️ Encryption: None (Cleartext)")
    st.sidebar.info("🌐 Port: 8080 (TCP)")
else:
    st.sidebar.success("✅ TLS: Active (TLSv1.3)")
    st.sidebar.info("🔒 Cipher: TLS_AES_256_GCM_SHA384")
    st.sidebar.info("🌐 Port: 8443 (TCP/TLS)")

col_client, col_network = st.columns(2)

with col_client:
    st.subheader("1. Client Application (User Form)")
    st.caption("Enter credentials to simulate sending an authentication request across the network.")
    
    with st.form("login_form"):
        username = st.text_input("Username", value="admin")
        password = st.text_input("Password", value="MySecretPassword@2026", type="password")
        token = st.text_input("Session Token", value="tok_sess_89a4bc12")
        submit_btn = st.form_submit_button("Transmit Packet 🚀")

with col_network:
    st.subheader("2. Network Channel / Interceptor View")
    st.caption("Simulated packet capture monitoring frames passing through the interface.")

    if submit_btn:
        with st.spinner("Transmitting packet over interface..."):
            time.sleep(0.6)

        raw_payload = f"username={username}&password={password}&session_token={token}"

        if "Plain" in protocol:
            st.error("🚨 PACKET INTERCEPTED: Cleartext HTTP Stream")
            st.markdown("**Captured Frame Details (Port 8080):**")
            
            http_frame = f"""POST /login HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: Mozilla/5.0 (ClientApp)
Content-Type: application/x-www-form-urlencoded
Content-Length: {len(raw_payload)}

{raw_payload}"""
            
            st.code(http_frame, language="http")
            
            st.warning("⚠️ **Security Breach Detected:** Sensitive credentials and session tokens are fully exposed to packet sniffers!")
            
        else:
           
            key = AESGCM.generate_key(bit_length=256)
            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            ciphertext = aesgcm.encrypt(nonce, raw_payload.encode('utf-8'), None)
            
            st.success("🔒 SECURE TRANSMISSION: TLS Cryptographic Session")
            st.markdown("**Captured Frame Details (Port 8443):**")
            
            tls_frame = f"""TLSv1.3 Record Layer: Application Data Protocol
Handshake Status: 1-RTT Complete (ECDHE Key Exchange)
Cipher Suite: TLS_AES_256_GCM_SHA384
Nonce/IV: {nonce.hex()}
Encrypted Payload (Ciphertext):
{ciphertext.hex()}"""
            
            st.code(tls_frame, language="text")
            
            st.info("✅ **Integrity & Confidentiality Guaranteed:** Data is completely unreadable without the negotiated ephemeral symmetric keys.")


st.markdown("---")
st.subheader("3. Security Posture Analysis")
st.table({
    "Security Vector": ["Confidentiality", "Data Integrity", "Server Authentication", "Vulnerability to Sniffing"],
    "Unsecured HTTP": ["❌ None (Cleartext ASCII)", "❌ Vulnerable to tampering", "❌ No verification", "🚨 High (Immediate leak)"],
    "HTTPS with TLS": ["✅ Strong (AES-GCM / ChaCha20)", "✅ Cryptographic MAC / AEAD", "✅ X.509 Certificate Chain", "🛡️ Immune to sniffing"]
})