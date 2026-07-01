import axiosInstance from '@/lib/axios';
import { API_ROUTES } from '@/config/routes';
import { 
  ReproductionRecordDto, 
  CreateRecordDto, 
  UpdateRecordDto, 
  RecordsResponseDto,
  StatisticsDto 
} from '@/api/dto/record.dto';

export interface GetRecordsParams {
  farm_id?: number;
  date_from?: string;
  date_to?: string;
  page?: number;
  limit?: number;
  sort?: string;
  order?: 'asc' | 'desc';
}

export const recordsApi = {
  getAll: (params?: GetRecordsParams) => 
    axiosInstance.get<RecordsResponseDto>(API_ROUTES.RECORDS, { params }),
  
  getById: (id: number) => 
    axiosInstance.get<ReproductionRecordDto>(`${API_ROUTES.RECORDS}/${id}`),
  
  create: (data: CreateRecordDto) => 
    axiosInstance.post<ReproductionRecordDto>(API_ROUTES.RECORDS, data),
  
  update: (id: number, data: UpdateRecordDto) => 
    axiosInstance.put<ReproductionRecordDto>(`${API_ROUTES.RECORDS}/${id}`, data),
  
  delete: (id: number) => 
    axiosInstance.delete(`${API_ROUTES.RECORDS}/${id}`),
  
  getStatistics: (params?: { farm_id?: number; date_from?: string; date_to?: string }) =>
    axiosInstance.get<StatisticsDto>(API_ROUTES.STATISTICS, { params }),
};