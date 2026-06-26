"use client";

import { useAuth } from "@/context/AuthContext";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  LogOut, User, BookOpen, Target,
  Trophy, AlertTriangle, CheckCircle2, ChevronRight, Code2
} from "lucide-react";

export default function Dashboard() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold text-indigo-600 tracking-tight">AI Career Agent</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm font-medium text-gray-700">{user.displayName}</span>
              <button
                onClick={logout}
                className="p-2 text-gray-400 hover:text-gray-500 rounded-full hover:bg-gray-100 transition-colors"
                title="Logout"
              >
                <LogOut size={20} />
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Profile & Summary Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

          {/* Profile Card */}
          <motion.div
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col items-center text-center"
          >
            <div className="h-24 w-24 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center mb-4 overflow-hidden">
              {user.photoURL ? (
                <img src={user.photoURL} alt="Profile" className="h-full w-full object-cover" />
              ) : (
                <User size={40} />
              )}
            </div>
            <h2 className="text-xl font-bold text-gray-900">{user.displayName}</h2>
            <p className="text-sm text-gray-500 mb-4">2nd Year BTech CSE • Tier-1</p>
            <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
              Level: Intermediate
            </div>
          </motion.div>

          {/* AI Summary */}
          <motion.div
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 md:col-span-2"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
              <Target className="text-indigo-500 mr-2" size={20} />
              AI Career Summary
            </h3>
            <p className="text-gray-600 leading-relaxed mb-4">
              You have a solid grasp of Python and OOP fundamentals but significant gaps in data structures and algorithms. With a placement goal 18 months away, you need structured, video-first DSA learning before tackling competitive programming.
            </p>
            <div className="bg-orange-50 border-l-4 border-orange-400 p-4 rounded-r-md">
              <div className="flex">
                <AlertTriangle className="h-5 w-5 text-orange-400" />
                <div className="ml-3">
                  <p className="text-sm text-orange-700 font-medium">
                    Recommended Action: Start Striver's A2Z DSA sheet from the Arrays section today.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Modules Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          {/* Module 1: Roadmap */}
          <motion.div
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer group"
          >
            <div className="flex justify-between items-start mb-4">
              <div className="bg-purple-100 p-3 rounded-lg text-purple-600">
                <Target size={24} />
              </div>
              <ChevronRight className="text-gray-400 group-hover:text-indigo-600 transition-colors" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-1">Career Roadmap</h3>
            <p className="text-sm text-gray-500 mb-4">Year-wise plan for AI/ML Placement</p>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-purple-600 h-2 rounded-full" style={{ width: '35%' }}></div>
            </div>
            <p className="text-xs text-right text-gray-500 mt-2">35% Completed</p>
          </motion.div>

          {/* Module 2: DSA Progress */}
          <motion.div
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer group"
          >
            <div className="flex justify-between items-start mb-4">
              <div className="bg-blue-100 p-3 rounded-lg text-blue-600">
                <Code2 size={24} />
              </div>
              <ChevronRight className="text-gray-400 group-hover:text-indigo-600 transition-colors" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-1">DSA Practice</h3>
            <p className="text-sm text-gray-500 mb-4">Arrays & Strings Focus</p>
            <div className="flex space-x-2 text-sm text-gray-600">
              <span className="flex items-center"><CheckCircle2 size={16} className="text-green-500 mr-1"/> 12 Solved</span>
              <span>•</span>
              <span className="flex items-center text-orange-500 font-medium"><Trophy size={16} className="mr-1"/> 3 Day Streak</span>
            </div>
          </motion.div>

          {/* Module 3: Course Recs */}
          <motion.div
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer group"
          >
            <div className="flex justify-between items-start mb-4">
              <div className="bg-green-100 p-3 rounded-lg text-green-600">
                <BookOpen size={24} />
              </div>
              <ChevronRight className="text-gray-400 group-hover:text-indigo-600 transition-colors" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-1">Recommended Courses</h3>
            <p className="text-sm text-gray-500 mb-4">Based on your weak areas</p>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-center"><span className="w-2 h-2 rounded-full bg-green-500 mr-2"></span> Intro to Dynamic Programming</li>
              <li className="flex items-center"><span className="w-2 h-2 rounded-full bg-green-500 mr-2"></span> Advanced Graph Algorithms</li>
            </ul>
          </motion.div>

        </div>
      </main>
    </div>
  );
}
