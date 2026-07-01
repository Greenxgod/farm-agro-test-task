import React from 'react';
import { ReproductionRecordDto } from '@/api/dto/record.dto';
import styles from './RecordsTable.module.css';

interface RecordsTableProps {
  records: ReproductionRecordDto[];
  onEdit: (record: ReproductionRecordDto) => void;
  onDelete: (id: number) => void;
  loading: boolean;
}

const RecordsTable: React.FC<RecordsTableProps> = ({
  records,
  onEdit,
  onDelete,
  loading,
}) => {
  if (loading) {
    return <div className={styles.loading}>Загрузка...</div>;
  }

  if (records.length === 0) {
    return <div className={styles.empty}>Нет записей</div>;
  }

  return (
    <div className={styles.container}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Дата</th>
            <th>Ферма</th>
            <th>Аборты</th>
            <th>Мертвые бычки</th>
            <th>Мертвые телки</th>
            <th>Стельность коров</th>
            <th>Стельность телок</th>
            <th>Воспр. коров</th>
            <th>Воспр. телок</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {records.map((record) => (
            <tr key={record.id}>
              <td>{new Date(record.date).toLocaleDateString('ru-RU')}</td>
              <td>{record.farm_name}</td>
              <td>{record.abort}</td>
              <td>{record.dead_bulls}</td>
              <td>{record.dead_heifers}</td>
              <td>{record.preg_rate_cows}%</td>
              <td>{record.preg_rate_heifers}%</td>
              <td>{record.reproduction_cows}</td>
              <td>{record.reproduction_heifers}</td>
              <td>
                <div className={styles.button_wrapper}>
                  <button
                    onClick={() => onEdit(record)}
                    className={styles.editBtn}
                  >
                    ✎
                  </button>
                  <button
                    onClick={() => onDelete(record.id)}
                    className={styles.deleteBtn}
                  >
                    ✕
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecordsTable;