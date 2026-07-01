export interface ReproductionRecordDto {
  id: number;
  farm_id: number;
  farm_name: string;
  date: string;
  abort: number;
  bulls_from_cows: number;
  bulls_from_heifers: number;
  conception_cows: number;
  conception_heifers: number;
  cows_from_cows: number;
  cows_from_heifers: number;
  dead_bulls: number;
  dead_heifers: number;
  preg_rate_cows: number;
  preg_rate_heifers: number;
  reproduction_cows: number;
  reproduction_heifers: number;
  created_at: string;
  updated_at: string;
}

export interface CreateRecordDto {
  farm_id: number;
  date: string;
  abort?: number;
  bulls_from_cows?: number;
  bulls_from_heifers?: number;
  conception_cows?: number;
  conception_heifers?: number;
  cows_from_cows?: number;
  cows_from_heifers?: number;
  dead_bulls?: number;
  dead_heifers?: number;
  preg_rate_cows?: number;
  preg_rate_heifers?: number;
  reproduction_cows?: number;
  reproduction_heifers?: number;
}

export interface UpdateRecordDto extends Partial<CreateRecordDto> {}

export interface PaginationDto {
  page: number;
  limit: number;
  total: number;
  pages: number;
}

export interface RecordsResponseDto {
  items: ReproductionRecordDto[];
  pagination: PaginationDto;
}

export interface StatisticsDto {
  total_records: number;
  total_abort: number;
  total_dead_bulls: number;
  total_dead_heifers: number;
  avg_preg_rate_cows: number;
  avg_preg_rate_heifers: number;
  total_bulls_from_cows: number;
  total_bulls_from_heifers: number;
  total_cows_from_cows: number;
  total_cows_from_heifers: number;
}