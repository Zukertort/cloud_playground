import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'

export interface DashboardData {
  ticker: string
  current_price: number
  signal: string
  confidence: number
  primary_signal: string
  history: Array<{ timestamp: string; close: number }>
  sentiment_score: number
  sentiment_analysis: string
  news_headlines: string[]
}

export const useDashboard = (ticker: string) => {
  return useQuery({
    queryKey: ['dashboard', ticker],
    queryFn: async () => {
      const { data } = await api.get<DashboardData>(`/dashboard/${ticker}`)
      return data
    },
    staleTime: 1000 * 60, 
    retry: 2 
  })
}

export interface TradePayload {
  ticker: string;
  side: "BUY" | "SELL";
  quantity: number;
  price: number;
}