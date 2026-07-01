import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { FarmDto } from '@/api/dto/farm.dto';
import { ReproductionRecordDto } from '@/api/dto/record.dto';
import { useCreateRecord, useUpdateRecord } from '@/hooks/useRecords';
import styles from './RecordForm.module.css';

const recordSchema = z.object({
  farm_id: z.number().min(1, 'Выберите ферму'),
  date: z.string().min(1, 'Выберите дату'),
  abort: z.number().min(0, 'Не может быть отрицательным').default(0),
  bulls_from_cows: z.number().min(0, 'Не может быть отрицательным').default(0),
  bulls_from_heifers: z.number().min(0, 'Не может быть отрицательным').default(0),
  conception_cows: z.number().min(0, 'Не может быть отрицательным').default(0),
  conception_heifers: z.number().min(0, 'Не может быть отрицательным').default(0),
  cows_from_cows: z.number().min(0, 'Не может быть отрицательным').default(0),
  cows_from_heifers: z.number().min(0, 'Не может быть отрицательным').default(0),
  dead_bulls: z.number().min(0, 'Не может быть отрицательным').default(0),
  dead_heifers: z.number().min(0, 'Не может быть отрицательным').default(0),
  preg_rate_cows: z.number().min(0, 'Не может быть отрицательным').max(100, 'Максимум 100').default(0),
  preg_rate_heifers: z.number().min(0, 'Не может быть отрицательным').max(100, 'Максимум 100').default(0),
  reproduction_cows: z.number().min(0, 'Не может быть отрицательным').default(0),
  reproduction_heifers: z.number().min(0, 'Не может быть отрицательным').default(0),
});

type RecordFormData = z.infer<typeof recordSchema>;

interface RecordFormProps {
  record?: ReproductionRecordDto | null;
  farms: FarmDto[];
  onClose: () => void;
  onSuccess: () => void;
}

const RecordForm: React.FC<RecordFormProps> = ({ record, farms, onClose, onSuccess }) => {
  const createMutation = useCreateRecord();
  const updateMutation = useUpdateRecord();
  const isEditing = !!record;

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<RecordFormData>({
    resolver: zodResolver(recordSchema),
    defaultValues: {
      farm_id: record?.farm_id || undefined,
      date: record?.date ? record.date.split('T')[0] : '',
      abort: record?.abort || 0,
      bulls_from_cows: record?.bulls_from_cows || 0,
      bulls_from_heifers: record?.bulls_from_heifers || 0,
      conception_cows: record?.conception_cows || 0,
      conception_heifers: record?.conception_heifers || 0,
      cows_from_cows: record?.cows_from_cows || 0,
      cows_from_heifers: record?.cows_from_heifers || 0,
      dead_bulls: record?.dead_bulls || 0,
      dead_heifers: record?.dead_heifers || 0,
      preg_rate_cows: record?.preg_rate_cows || 0,
      preg_rate_heifers: record?.preg_rate_heifers || 0,
      reproduction_cows: record?.reproduction_cows || 0,
      reproduction_heifers: record?.reproduction_heifers || 0,
    },
  });

  const onSubmit = async (data: RecordFormData) => {
    try {
      if (isEditing && record) {
        await updateMutation.mutateAsync({ id: record.id, data });
      } else {
        await createMutation.mutateAsync(data);
      }
      onSuccess();
    } catch (error: any) {
      if (error.errors) {
        Object.entries(error.errors).forEach(([key, value]) => {
          setError(key as any, { message: Array.isArray(value) ? value[0] : String(value) });
        });
      }
    }
  };

  const fields = [
    { name: 'abort', label: 'Аборты' },
    { name: 'bulls_from_cows', label: 'Бычки от коров' },
    { name: 'bulls_from_heifers', label: 'Бычки от телок' },
    { name: 'conception_cows', label: 'Осеменение коров' },
    { name: 'conception_heifers', label: 'Осеменение телок' },
    { name: 'cows_from_cows', label: 'Телочки от коров' },
    { name: 'cows_from_heifers', label: 'Телочки от телок' },
    { name: 'dead_bulls', label: 'Мертвые бычки' },
    { name: 'dead_heifers', label: 'Мертвые телки' },
    { name: 'preg_rate_cows', label: 'Стельность коров %' },
    { name: 'preg_rate_heifers', label: 'Стельность телок %' },
    { name: 'reproduction_cows', label: 'Воспр. коров' },
    { name: 'reproduction_heifers', label: 'Воспр. телок' },
  ];

  return (
    <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
      <div className={styles.row}>
        <div className={styles.field}>
          <label className={styles.label}>Ферма *</label>
          <select {...register('farm_id', { valueAsNumber: true })} className={styles.select}>
            <option value="">Выберите ферму</option>
            {farms.map((farm) => (
              <option key={farm.id} value={farm.id}>
                {farm.name}
              </option>
            ))}
          </select>
          {errors.farm_id && <span className={styles.error}>{errors.farm_id.message}</span>}
        </div>

        <div className={styles.field}>
          <label className={styles.label}>Дата *</label>
          <input type="date" {...register('date')} className={styles.input} />
          {errors.date && <span className={styles.error}>{errors.date.message}</span>}
        </div>
      </div>

      <div className={styles.grid}>
        {fields.map(({ name, label }) => (
          <div key={name} className={styles.field}>
            <label className={styles.label}>{label}</label>
            <input
              type="number"
              step={name.includes('preg_rate') ? '0.01' : '1'}
              {...register(name as any, { valueAsNumber: true })}
              className={styles.input}
            />
            {errors[name as keyof RecordFormData] && (
              <span className={styles.error}>{errors[name as keyof RecordFormData]?.message}</span>
            )}
          </div>
        ))}
      </div>

      <div className={styles.actions}>
        <button type="button" onClick={onClose} className={styles.cancelBtn}>
          Отмена
        </button>
        <button type="submit" disabled={isSubmitting} className={styles.submitBtn}>
          {isSubmitting ? 'Сохранение...' : isEditing ? 'Обновить' : 'Создать'}
        </button>
      </div>
    </form>
  );
};

export default RecordForm;