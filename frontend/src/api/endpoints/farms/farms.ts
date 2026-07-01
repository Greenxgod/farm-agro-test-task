import axiosInstance from '@/lib/axios';
import { API_ROUTES } from '@/config/routes';
import { FarmDto, CreateFarmDto, UpdateFarmDto } from '@/api/dto/farm.dto';

export const farmsApi = {
  getAll: () => axiosInstance.get<FarmDto[]>(API_ROUTES.FARMS),
  
  getById: (id: number) => axiosInstance.get<FarmDto>(`${API_ROUTES.FARMS}/${id}`),
  
  create: (data: CreateFarmDto) => axiosInstance.post<FarmDto>(API_ROUTES.FARMS, data),
  
  update: (id: number, data: UpdateFarmDto) => 
    axiosInstance.put<FarmDto>(`${API_ROUTES.FARMS}/${id}`, data),
  
  delete: (id: number) => axiosInstance.delete(`${API_ROUTES.FARMS}/${id}`),
};