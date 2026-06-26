import { initializeApp, getApps } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCbedRwn4rqEZRpSR_aOQmxQ1hLDgTKdPA",
  authDomain: "ai-career-agent-cd5b8.firebaseapp.com",
  projectId: "ai-career-agent-cd5b8",
  storageBucket: "ai-career-agent-cd5b8.firebasestorage.app",
  messagingSenderId: "88378131150",
  appId: "1:88378131150:web:81b3bd2a39e6e00cebc69f",
  measurementId: "G-8K782KJS06"
};

// Initialize Firebase only if it hasn't been initialized already
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
const auth = getAuth(app);

export { app, auth };
