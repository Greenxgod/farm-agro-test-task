import React from 'react';
import { StatisticsDto } from '@/api/dto/record.dto';
import styles from './Statistics.module.css';

interface StatisticsProps {
  stats: StatisticsDto | null;
  loading: boolean;
}

const Statistics: React.FC<StatisticsProps> = ({ stats, loading }) => {
  if (loading) {
    return <div className={styles.skeleton}>Загрузка статистики...</div>;
  }

  if (!stats) {
    return null;
  }

  const items = [
    { label: 'Всего записей', value: stats.total_records },
    { label: 'Всего абортов', value: stats.total_abort },
    { label: 'Мертвых бычков', value: stats.total_dead_bulls },
    { label: 'Мертвых телок', value: stats.total_dead_heifers },
    { label: 'Ср. стельность коров', value: `${stats.avg_preg_rate_cows}%` },
    { label: 'Ср. стельность телок', value: `${stats.avg_preg_rate_heifers}%` },
    { label: 'Бычки от коров', value: stats.total_bulls_from_cows },
    { label: 'Бычки от телок', value: stats.total_bulls_from_heifers },
    { label: 'Телочки от коров', value: stats.total_cows_from_cows },
    { label: 'Телочки от телок', value: stats.total_cows_from_heifers },
  ];

  return (
    <div className={styles.container}>
      {items.map((item) => (
        <div key={item.label} className={styles.card}>
          <div className={styles.label}>{item.label}</div>
          <div className={styles.value}>{item.value}</div>
        </div>
      ))}
    </div>
  );
};

export default Statistics;