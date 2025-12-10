import { useNavigate } from '@tanstack/react-router'
import { TrendingUp, Activity, AlertCircle } from 'lucide-react'

export const MarketWidget = () => {
  const navigate = useNavigate()

  // Hardcoded for now, later fetch from API
  const topPicks = [
    { ticker: "AAPL", signal: "BUY", conf: "83%" },
    { ticker: "MSFT", signal: "IGNORE", conf: "45%" },
    { ticker: "GOOGL", signal: "BUY", conf: "89%" }
  ]

  return (
    <div className="flex w-full max-w-4xl mx-auto mt-6 mb-6 flex-col gap-y-4">
      <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-100">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-700 flex items-center gap-2">
            <Activity className="text-blue-600" />
            Quant Market Pulse
          </h2>
          <button 
            onClick={() => navigate({ to: '/dashboard' })}
            className="text-sm text-blue-600 font-semibold hover:underline"
          >
            Open Trading Terminal →
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {topPicks.map((pick) => (
            <div 
              key={pick.ticker}
              onClick={() => navigate({ to: `/dashboard`, search: { ticker: pick.ticker } })} 
              className="cursor-pointer hover:bg-gray-50 p-3 rounded-md border border-gray-200 flex justify-between items-center transition-all"
            >
              <div>
                <span className="font-bold text-gray-900">{pick.ticker}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={`px-2 py-1 rounded text-xs font-bold ${
                  pick.signal === "BUY" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"
                }`}>
                  {pick.signal}
                </span>
                <span className="text-xs text-gray-500">{pick.conf}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}