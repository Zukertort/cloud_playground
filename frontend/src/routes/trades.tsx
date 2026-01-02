import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { Table, Badge, Spinner, Box} from '@chakra-ui/react'

export const Route = createFileRoute('/trades')({
  component: TradesPage,
})

interface Trade {
  id: number
  ticker: string
  side: string
  quantity: number
  price: number
  timestamp: string
  status: string
}

function TradesPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['trades'],
    queryFn: async () => {
      const res = await api.get<Trade[]>('/trade/history')
      return res.data
    }
  })

  if (isLoading) return <Box p={10} textAlign="center"><Spinner /></Box>

  return (
    <div className="p-6 max-w-7xl mx-auto w-full text-gray-800">
      <h1 className="text-3xl font-bold text-gray-700 mb-6">Execution History</h1>
      
      <div className="bg-white rounded-lg shadow overflow-hidden border border-gray-100">
        <Table.Root size="md" variant={'outline'} bg="white" color="gray.800">
          <Table.Header>
            <Table.Row bg="cyan.500">
              <Table.ColumnHeader>Date</Table.ColumnHeader>
              <Table.ColumnHeader>Ticker</Table.ColumnHeader>
              <Table.ColumnHeader>Side</Table.ColumnHeader>
              <Table.ColumnHeader>Qty</Table.ColumnHeader>
              <Table.ColumnHeader>Price</Table.ColumnHeader>
              <Table.ColumnHeader>Status</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {data?.map((trade) => (
              <Table.Row key={trade.id} _hover={{ bg: "gray.300" }}>
                <Table.Cell>{new Date(trade.timestamp).toLocaleString()}</Table.Cell>
                <Table.Cell fontWeight="bold">{trade.ticker}</Table.Cell>
                <Table.Cell>
                  <Badge colorPalette={trade.side === 'BUY' ? 'green' : 'red'}>
                    {trade.side}
                  </Badge>
                </Table.Cell>
                <Table.Cell>{trade.quantity}</Table.Cell>
                <Table.Cell>${trade.price.toFixed(2)}</Table.Cell>
                <Table.Cell>
                   <Badge variant="outline" colorPalette="blue">{trade.status}</Badge>
                </Table.Cell>
              </Table.Row>
            ))}
            {data?.length === 0 && (
                <Table.Row><Table.Cell colSpan={6} textAlign="center">No trades executed yet.</Table.Cell></Table.Row>
            )}
          </Table.Body>
        </Table.Root>
      </div>
    </div>
  )
}