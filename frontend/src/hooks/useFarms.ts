import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { farmsApi } from '@/api/endpoints/farms/farms';

export const useFarms = () => {
  return useQuery({
    queryKey: ['farms'],
    queryFn: async () => {
      const response = await farmsApi.getAll();
      return response.data;
    },
  });
};

export const useCreateFarm = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: farmsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farms'] });
    },
  });
};

export const useUpdateFarm = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: { name: string } }) =>
      farmsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farms'] });
    },
  });
};

export const useDeleteFarm = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: farmsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farms'] });
    },
  });
};