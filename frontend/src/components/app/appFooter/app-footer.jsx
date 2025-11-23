import styles from './app-footer.module.css';

const AppFooter = ({ className }) => {
    return (
        <footer className={`${styles['app-footer']} ${className || ''}`}>
            <div className={styles['app-footer__logo']}>
                <img src="/logo.svg" />
                per aspera ad – astra
            </div>
            <p className={styles['app-footer__caption']}>
                Kseniia Shlenskaia | ⓒ 2025
            </p>
        </footer>
    );
}

export default AppFooter;