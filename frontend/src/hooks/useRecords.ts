import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { recordsApi, GetRecordsParams } from '@/api/endpoints/records/records';
import { CreateRecordDto, UpdateRecordDto } from '@/api/dto/record.dto';

export const useRecords = (params?: GetRecordsParams) => {
  return useQuery({
    queryKey: ['records', params],
    queryFn: async () => {
      const response = await recordsApi.getAll(params);
      return response.data;
    },
  });
};

export const useStatistics = (farmId?: number, dateFrom?: string, dateTo?: string) => {
  return useQuery({
    queryKey: ['statistics', farmId, dateFrom, dateTo],
    queryFn: async () => {
      const response = await recordsApi.getStatistics({ farm_id: farmId, date_from: dateFrom, date_to: dateTo });
      return response.data;
    },
  });
};

export const useCreateRecord = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateRecordDto) => recordsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['records'] });
      queryClient.invalidateQueries({ queryKey: ['statistics'] });
    },
  });
};

export const useUpdateRecord = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateRecordDto }) =>
      recordsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['records'] });
      queryClient.invalidateQueries({ queryKey: ['statistics'] });
    },
  });
};

export const useDeleteRecord = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: recordsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['records'] });
      queryClient.invalidateQueries({ queryKey: ['statistics'] });
    },
  });
};