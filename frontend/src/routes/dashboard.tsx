import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { createFileRoute } from '@tanstack/react-router'
import { useDashboard, type TradePayload, type DashboardData } from '../hooks/useDashboard'
import { Button } from "@chakra-ui/react"
import api from '../lib/api'
//import { Toaster } from "../components/ui/toaster"

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

const handleTrade = async (data: DashboardData, side: "BUY" | "SELL") => {
  if (!data) return;

  const payload: TradePayload = {
    ticker: data.ticker,
    side: side,
    quantity: 10,
    price: data.current_price
  };

  try {
    console.log(`Sending ${side} order for ${data.ticker}...`);
 
    const response = await api.post('/trade/execute', payload);
    
    console.log("Trade Executed:", response.data);
    alert(`Success! Trade ID: ${response.data.id} Status: ${response.data.status}`);
    
  } catch (error: any) {
    console.error("Execution Failed:", error);
    alert(`Execution Failed: ${error.response?.data?.detail || error.message}`);
  }
};

function DashboardPage() {
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
          <br/>
          <Button 
            size="xs" 
            colorPalette='green' 
            variant='solid'
            onClick={() => handleTrade(data, 'BUY')}
            >Buy
          </Button>
          <Button 
            size="xs" 
            colorPalette='red'
            variant='surface'
            marginLeft={2}
            onClick={() => handleTrade(data, 'SELL')}
            >Sell
          </Button>
        </div>

        <div className={`p-4 rounded-xl shadow-sm border ${data.signal === 'BUY' ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
          }`}>
          <p className="text-xs font-bold uppercase tracking-wider text-gray-500">AI Signal</p>
          <div className="flex items-baseline gap-2">
            <h2 className={`text-2xl font-black ${data.signal === 'BUY' ? 'text-green-700' : 'text-gray-700'
              }`}>
              {data.signal}
            </h2>
            <span className="text-sm font-semibold text-gray-600">
              {isNaN(data.confidence) ? "0.0" : (data.confidence * 100).toFixed(1)}% Conf.
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-1">Meta-Model Logic</p>
        </div>

        <div className={`p-4 rounded-xl shadow-sm border ${data.sentiment_score > 0 ? 'bg-blue-50 border-blue-200' :
          data.sentiment_score < 0 ? 'bg-red-50 border-red-200' : 'bg-gray-50 border-gray-200'
          }`}>
          <p className="text-xs font-bold uppercase tracking-wider text-gray-500">Market Sentiment</p>
          <div className="flex items-baseline gap-2">
            <h2 className={`text-2xl font-black ${data.sentiment_score > 0 ? 'text-blue-700' :
              data.sentiment_score < 0 ? 'text-red-700' : 'text-gray-700'
              }`}>
              {data.sentiment_analysis}
            </h2>
            <span className="text-sm font-semibold text-gray-600">
              {data.sentiment_score > 0 ? '+' : ''}{data.sentiment_score.toFixed(2)}
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-1">AI Analysis (Gemini Flash)</p>
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

      <div className="mt-6 grid grid-cols-1 gap-4">
        <h3 className="text-lg font-bold text-gray-800">Latest Intelligence</h3>
        {data.news_headlines.map((news, i) => (
          <div key={i} className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm flex items-center gap-3">
            <span className="text-xl">📰</span>
            <p className="text-sm text-gray-600 font-medium">{news}</p>
          </div>
        ))}
      </div>
    </div>
  )
}