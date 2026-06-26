"use client";

import { useAuth } from "@/context/AuthContext";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Bot, Sparkles, Code2, ArrowRight } from "lucide-react";

export default function Home() {
  const { user, loading, signInWithGoogle } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (user) {
      router.push("/dashboard");
    }
  }, [user, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100"
      >
        <div className="p-8">
          <div className="flex justify-center mb-6">
            <div className="bg-indigo-100 p-3 rounded-full text-indigo-600">
              <Bot size={32} />
            </div>
          </div>

          <h1 className="text-3xl font-extrabold text-center text-gray-900 mb-2">
            AI Career Agent
          </h1>
          <p className="text-center text-gray-500 mb-8">
            Personalised career guidance for BTech CS students
          </p>

          <div className="space-y-4 mb-8">
            <div className="flex items-center text-sm text-gray-600">
              <Sparkles className="text-indigo-500 mr-3" size={20} />
              <span>AI-driven skill assessment & roadmaps</span>
            </div>
            <div className="flex items-center text-sm text-gray-600">
              <Code2 className="text-indigo-500 mr-3" size={20} />
              <span>Curated DSA & LeetCode sheets</span>
            </div>
          </div>

          <button
            onClick={signInWithGoogle}
            className="w-full flex items-center justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
          >
            Continue with Google
            <ArrowRight className="ml-2" size={16} />
          </button>
        </div>
        <div className="bg-gray-50 px-8 py-4 border-t border-gray-100 text-center text-xs text-gray-500">
          Built exclusively for India's BTech CS community
        </div>
      </motion.div>
    </div>
  );
}
