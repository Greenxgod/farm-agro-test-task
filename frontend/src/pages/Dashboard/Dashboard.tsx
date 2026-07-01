import React, { useState } from 'react';
import { useFarms } from '@/hooks/useFarms';
import { useRecords, useStatistics, useDeleteRecord } from '@/hooks/useRecords';
import { ReproductionRecordDto } from '@/api/dto/record.dto';
import Header from '@/components/Header/Header';
import Statistics from '@/components/Statistics/Statistics';
import Filters from '@/components/Filters/Filters';
import RecordsTable from '@/components/RecordsTable/RecordsTable';
import Pagination from '@/components/Pagination/Pagination';
import Modal from '@/components/Modal/Modal';
import RecordForm from '@/components/RecordForm/RecordForm';
import FarmManagement from '@/components/FarmManagement/FarmManagement';
import styles from './Dashboard.module.css';

const Dashboard: React.FC = () => {
  const [filters, setFilters] = useState({
    farm_id: undefined as number | undefined,
    date_from: '',
    date_to: '',
    page: 1,
    limit: 20,
  });

  const [isRecordFormOpen, setIsRecordFormOpen] = useState(false);
  const [isFarmManagementOpen, setIsFarmManagementOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState<ReproductionRecordDto | null>(null);

  const { data: farms } = useFarms();
  const { data: recordsData, isLoading: recordsLoading, refetch } = useRecords(filters);
  const { data: stats, isLoading: statsLoading } = useStatistics(
    filters.farm_id,
    filters.date_from || undefined,
    filters.date_to || undefined
  );

  const deleteMutation = useDeleteRecord();

  const handleFilterChange = (key: string, value: any) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
  };

  const handlePageChange = (page: number) => {
    setFilters((prev) => ({ ...prev, page }));
  };

  const handleLimitChange = (limit: number) => {
    setFilters((prev) => ({ ...prev, limit, page: 1 }));
  };

  const handleEdit = (record: ReproductionRecordDto) => {
    setEditingRecord(record);
    setIsRecordFormOpen(true);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Удалить эту запись?')) {
      deleteMutation.mutate(id, {
        onSuccess: () => refetch(),
      });
    }
  };

  const handleFormClose = () => {
    setIsRecordFormOpen(false);
    setEditingRecord(null);
  };

  const handleFormSuccess = () => {
    handleFormClose();
    refetch();
  };

  const handleFarmManagementClose = () => {
    setIsFarmManagementOpen(false);
  };

  const handleFarmManagementSuccess = () => {
    refetch();
  };

  const clearFilters = () => {
    setFilters({
      farm_id: undefined,
      date_from: '',
      date_to: '',
      page: 1,
      limit: 20,
    });
  };

  return (
    <div className={styles.page}>
      <Header
        onAddRecord={() => {
          setEditingRecord(null);
          setIsRecordFormOpen(true);
        }}
        onManageFarms={() => setIsFarmManagementOpen(true)}
      />

      <div className={styles.content}>
        <Statistics stats={stats || null} loading={statsLoading} />

        {farms && (
          <Filters
            farms={farms}
            selectedFarm={filters.farm_id?.toString() || ''}
            dateFrom={filters.date_from}
            dateTo={filters.date_to}
            onFarmChange={(value) => handleFilterChange('farm_id', value ? Number(value) : undefined)}
            onDateFromChange={(value) => handleFilterChange('date_from', value)}
            onDateToChange={(value) => handleFilterChange('date_to', value)}
            onClear={clearFilters}
          />
        )}

        <RecordsTable
          records={recordsData?.items || []}
          onEdit={handleEdit}
          onDelete={handleDelete}
          loading={recordsLoading}
        />

        {recordsData && (
          <Pagination
            currentPage={recordsData.pagination.page}
            totalPages={recordsData.pagination.pages}
            limit={recordsData.pagination.limit}
            total={recordsData.pagination.total}
            onPageChange={handlePageChange}
            onLimitChange={handleLimitChange}
          />
        )}
      </div>

      <Modal
        isOpen={isRecordFormOpen}
        onClose={handleFormClose}
        title={editingRecord ? 'Редактирование записи' : 'Новая запись'}
      >
        <RecordForm
          record={editingRecord}
          farms={farms || []}
          onClose={handleFormClose}
          onSuccess={handleFormSuccess}
        />
      </Modal>

      <Modal
        isOpen={isFarmManagementOpen}
        onClose={handleFarmManagementClose}
        title="Управление фермами"
      >
        <FarmManagement
          farms={farms || []}
          onClose={handleFarmManagementClose}
          onSuccess={handleFarmManagementSuccess}
        />
      </Modal>
    </div>
  );
};

export default Dashboard;