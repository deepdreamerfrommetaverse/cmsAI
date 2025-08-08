import { useEffect, useState } from 'react';
import api from "@/lib/api";
interface RevenueData {
  total: number;
  currency: string;
  error?: string;
}

export function useStripe() {
  const [revenue, setRevenue] = useState<RevenueData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRevenue = async () => {
      try {
        const res = await api.get<RevenueData>('/stripe/revenue');
        setRevenue(res.data);
        if (res.data.error) {
          setError(res.data.error);
        }
      } catch (err) {
        console.error('Failed to fetch Stripe revenue:', err);
        setError('Failed to load revenue data');
      }
    };
    if (revenue === null) {
      fetchRevenue();
    }
  }, [revenue]);

  return { revenue, error };
}
