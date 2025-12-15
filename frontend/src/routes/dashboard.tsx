import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { useSearch, createFileRoute } from '@tanstack/react-router'
import { useDashboard } from '../hooks/useDashboard'

interface DashboardSearch {
  ticker?: string
}

export const Route = createFileRoute('/dashboard')({
  component: DashboardPage,
  validateSearch: (search: Record<string, unknown>): DashboardSearch => {
    return {
      ticker: (search.ticker as string) || 'AAPL',
    }
  },
})

function DashboardPage() {
  // Now we get type-safe search params from the Route
  const { ticker } = Route.useSearch()

  const { data, isLoading, error } = useDashboard(ticker || 'AAPL')

  if (isLoading) return <div className="p-10 text-center">Loading Alpha...</div>
  if (error) return <div className="p-10 text-center text-red-500">Error: {error.message}</div>
  if (!data) return null

  return (
    <div className="p-6 max-w-7xl mx-auto w-full">
      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{data.ticker}</h1>
          <p className="text-gray-500">${data.current_price.toFixed(2)}</p>
        </div>
        
        <div className={`p-4 rounded-xl shadow-sm border ${
            data.signal === 'BUY' ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
        }`}>
          <p className="text-xs font-bold uppercase tracking-wider text-gray-500">AI Signal</p>
          <div className="flex items-baseline gap-2">
            <h2 className={`text-2xl font-black ${
                data.signal === 'BUY' ? 'text-green-700' : 'text-gray-700'
            }`}>
                {data.signal}
            </h2>
            <span className="text-sm font-semibold text-gray-600">
              {isNaN(data.meta_confidence) ? "0.0" : (data.meta_confidence * 100).toFixed(1)}% Conf.
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-1">Meta-Model Logic</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data.history}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis 
                dataKey="timestamp" 
                tickFormatter={(str) => new Date(str).toLocaleDateString()}
                minTickGap={30}
            />
            <YAxis domain={['auto', 'auto']} />
            <Tooltip 
                labelFormatter={(label) => new Date(label).toLocaleString()}
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Line 
              type="monotone" 
              dataKey="close" 
              stroke="#2563eb" 
              strokeWidth={2} 
              dot={false} 
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}