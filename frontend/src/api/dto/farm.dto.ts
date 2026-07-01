export interface FarmDto {
  id: number;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface CreateFarmDto {
  name: string;
}

export interface UpdateFarmDto {
  name: string;
}