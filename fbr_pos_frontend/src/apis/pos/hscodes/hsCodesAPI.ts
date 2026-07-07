import axiosInstance from '@/apis/axiosInstance'

export interface HSCode {
  id: number
  code: string
  description: string
  default_rate: string | null
  uom: string | null
}

export interface PaginatedHSCodes {
  count: number
  next: string | null
  previous: string | null
  results: HSCode[]
}

export const hsCodesAPI = {
  fetchHSCodes: async (page = 1, search = ''): Promise<PaginatedHSCodes> => {
    const response = await axiosInstance.get('/hs-codes/', {
      params: {
        page,
        search
      }
    })
    return response.data
  }
}
