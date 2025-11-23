import styles from './app-header.module.css';

import AppHeaderLink from './app-header-link';

const AppHeader = ({ className }) => {
    return (
        <header className={`${styles['app-header']} ${className || ''}`}>

            <div className={styles['app-header__logo']}>
                <img src="/logo-small.svg" />
                ASTRA
            </div>

            <nav className={styles['app-header__nav']}>
                <AppHeaderLink
                    href='/'
                    className={styles['app-header__nav-link']}
                >
                    Dashboard
                </AppHeaderLink>
                <AppHeaderLink
                    href='/analysis'
                    className={styles['app-header__nav-link']}
                >
                    ASTRA Analysis
                </AppHeaderLink>
                <AppHeaderLink
                    href='/statistics'
                    className={styles['app-header__nav-link']}
                >
                    Statistics
                </AppHeaderLink>
            </nav>

            <div className={styles['app-header__avatar']}>
                <div className={styles['app-header__avatar-icon']}>KS</div>
                <div className={styles['app-header__avatar-text']}>
                    <p>Kseniia Shlenskaia</p>
                    <p>Team #9</p>
                </div>
            </div>

        </header>
    );
}

export default AppHeader;