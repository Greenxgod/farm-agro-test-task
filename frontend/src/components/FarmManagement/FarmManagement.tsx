import React, { useState } from 'react';
import { FarmDto } from '@/api/dto/farm.dto';
import { useCreateFarm, useUpdateFarm, useDeleteFarm } from '@/hooks/useFarms';
import styles from './FarmManagement.module.css';

interface FarmManagementProps {
  farms: FarmDto[];
  onClose: () => void;
  onSuccess: () => void;
}

const FarmManagement: React.FC<FarmManagementProps> = ({ farms, onSuccess }) => {
  const [newName, setNewName] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingName, setEditingName] = useState('');
  const [error, setError] = useState<string | null>(null);

  const createMutation = useCreateFarm();
  const updateMutation = useUpdateFarm();
  const deleteMutation = useDeleteFarm();

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    setError(null);
    try {
      await createMutation.mutateAsync({ name: newName.trim() });
      setNewName('');
      onSuccess();
    } catch (err: any) {
      setError(err.message || 'Ошибка создания фермы');
    }
  };

  const handleUpdate = async (id: number) => {
    if (!editingName.trim()) return;
    setError(null);
    try {
      await updateMutation.mutateAsync({ id, data: { name: editingName.trim() } });
      setEditingId(null);
      setEditingName('');
      onSuccess();
    } catch (err: any) {
      setError(err.message || 'Ошибка обновления фермы');
    }
  };

  const handleDelete = async (id: number, name: string) => {
    if (window.confirm(`Удалить ферму "${name}"?\n\nВсе связанные записи будут удалены автоматически.`)) {
      setError(null);
      try {
        await deleteMutation.mutateAsync(id);
        onSuccess();
      } catch (err: any) {
        setError(err.message || 'Ошибка удаления фермы');
      }
    }
  };

  return (
    <div className={styles.container}>
      {error && (
        <div className={styles.error}>
          ⚠️ {error}
        </div>
      )}

      <form onSubmit={handleCreate} className={styles.createForm}>
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="Название фермы"
          className={styles.input}
        />
        <button type="submit" disabled={!newName.trim()} className={styles.addBtn}>
          Добавить
        </button>
      </form>

      <div className={styles.list}>
        {farms.map((farm) => (
          <div key={farm.id} className={styles.item}>
            {editingId === farm.id ? (
              <>
                <input
                  type="text"
                  value={editingName}
                  onChange={(e) => setEditingName(e.target.value)}
                  className={styles.input}
                />
                <button onClick={() => handleUpdate(farm.id)} className={styles.saveBtn}>
                  Сохранить
                </button>
                <button onClick={() => setEditingId(null)} className={styles.cancelBtn}>
                  Отмена
                </button>
              </>
            ) : (
              <>
                <span className={styles.name}>{farm.name}</span>
                <div className={styles.actions}>
                  <button
                    onClick={() => {
                      setEditingId(farm.id);
                      setEditingName(farm.name);
                    }}
                    className={styles.editBtn}
                  >
                    ✎
                  </button>
                  <button
                    onClick={() => handleDelete(farm.id, farm.name)}
                    className={styles.deleteBtn}
                  >
                    ✕
                  </button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FarmManagement;