import styles from './app-header.module.css';

const AppHeaderLogin = ({ className, state = '' }) => {
    return (
        <header className={`${styles['app-header']} ${styles['app-header--login']} ${className || ''}`}>
            <div className={`${styles['app-header__logo']} ${styles['app-header__logo--full']}`}>
                <img src="/logo.svg" />
                astra
            </div>
        </header>
    );
}

export default AppHeaderLogin;