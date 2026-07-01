import React from 'react';
import styles from './Header.module.css';

interface HeaderProps {
  onAddRecord: () => void;
  onManageFarms: () => void;
}

const Header: React.FC<HeaderProps> = ({ onAddRecord, onManageFarms }) => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <h1 className={styles.title}>🐄 Репродуктивные показатели ферм</h1>
        <div className={styles.actions}>
          <button className={styles.btnPrimary} onClick={onAddRecord}>
            Добавить запись
          </button>
          <button className={styles.btnSecondary} onClick={onManageFarms}>
            Управление фермами
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;