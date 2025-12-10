import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'

interface DashboardData {
  ticker: string
  current_price: number
  signal: string
  meta_confidence: number
  primary_signal: string
  history: Array<{ timestamp: string; close: number }>
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