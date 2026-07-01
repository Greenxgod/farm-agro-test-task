import React from 'react';
import { FarmDto } from '@/api/dto/farm.dto';
import styles from './Filters.module.css';

interface FiltersProps {
  farms: FarmDto[];
  selectedFarm: string;
  dateFrom: string;
  dateTo: string;
  onFarmChange: (value: string) => void;
  onDateFromChange: (value: string) => void;
  onDateToChange: (value: string) => void;
  onClear: () => void;
}

const Filters: React.FC<FiltersProps> = ({
  farms,
  selectedFarm,
  dateFrom,
  dateTo,
  onFarmChange,
  onDateFromChange,
  onDateToChange,
  onClear,
}) => {
  return (
    <div className={styles.container}>
      <div className={styles.group}>
        <label className={styles.label}>Ферма</label>
        <select
          value={selectedFarm}
          onChange={(e) => onFarmChange(e.target.value)}
          className={styles.select}
        >
          <option value="">Все фермы</option>
          {farms.map((farm) => (
            <option key={farm.id} value={farm.id}>
              {farm.name}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.group}>
        <label className={styles.label}>Дата с</label>
        <input
          type="date"
          value={dateFrom}
          onChange={(e) => onDateFromChange(e.target.value)}
          className={styles.input}
        />
      </div>

      <div className={styles.group}>
        <label className={styles.label}>Дата по</label>
        <input
          type="date"
          value={dateTo}
          onChange={(e) => onDateToChange(e.target.value)}
          className={styles.input}
        />
      </div>

      <button onClick={onClear} className={styles.clearBtn}>
        Очистить
      </button>
    </div>
  );
};

export default Filters;