import sys
from ConfigManager import ConfigManager
from DnsResolver import DnsResolver
from Logger import Logger
from Sniffer import Sniffer
from LibraryChecker import LibraryChecker


def main():
    logger = Logger()

    logger.log("INFO", "Uruchamianie PyTraffic...")

    checker = LibraryChecker()

    if not checker.are_all_libraries_installed():
        logger.log("ERROR", "Zainstaluj wymagane biblioteki:")
        for lib in checker.get_missing_libraries():
            logger.log("ERROR", f"- {lib}")
        logger.log("ERROR", "Zamykam program z powodu błędu.")
        sys.exit(1)

    logger.log("INFO", "Wczytywanie konfiguracji...")

    config_manager = ConfigManager()

    if config_manager.config_exists():
        try:
            config_manager.load_config()
            unsafe_domains = config_manager.get_unsafe_domains()
            logger.log("INFO", f"Wczytano ({len(unsafe_domains)}) niebezpieczne domeny.")
        except RuntimeError as e:
            logger.log("ERROR", f"Nie udało się wczytać konfiguracji: {e}")
            logger.log("ERROR", "Zamykam program z powodu błędu.")
            sys.exit(1)
    else:
        config_manager.create_default_config()
        logger.log(
            "WARNING",
            f"Stworzono nową domyślną konfigurację z domenami: {', '.join(config_manager.DEFAULT_DOMAINS)} w {config_manager.get_config_file_path()}"
        )

    logger.log("INFO", "Rozwiązywanie domen...")
    resolver = DnsResolver()
    resolved_ips = []

    unsafe_domains = config_manager.get_unsafe_domains()
    for domain in unsafe_domains:
        try:
            ip = resolver.resolve_domain(domain)
            resolved_ips.append(ip)
        except RuntimeError as e:
            logger.log("ERROR", f"Nie udało się rozwiązać domeny '{domain}': {e}")
            logger.log("ERROR", "Zamykam program z powodu błędu.")
            sys.exit(1)

    logger.log("INFO", "Zbieranie interfejsów...")
    sniffer = Sniffer()
    try:
        interfaces = sniffer.get_available_interfaces()
        if not interfaces:
            logger.log("ERROR", "Nie znaleziono żadnych interfejsów sieciowych. Zamykam program.")
            sys.exit(1)

        logger.log("WARNING", f"Dostępne interfejsy sieciowe(1-{sniffer.get_number_of_available_interfaces()}):")
        for iface in interfaces:
            logger.log("WARNING", f"{iface['index']}. {iface['name']}")
    except RuntimeError as e:
        logger.log("ERROR", f"Nie udało się pobrać listy interfejsów: {e}")
        sys.exit(1)

    #Loop
    while True:
        try:
            yellow = "\033[33m"
            reset = "\033[0m"
            choice_input = input(f"{yellow}Wybierz numer interfejsu do monitorowania(domyślnie 1): {reset}")

            if not choice_input:
                choice = 1
            else:
                choice = int(choice_input)

            selected_interface = next((iface for iface in interfaces if iface["index"] == choice), None)

            if selected_interface:
                logger.log("WARNING", f"Wybrano interfejs: {selected_interface['name']}")
                try:
                    sniffer.start_sniffing(selected_interface["name"], resolved_ips)
                except RuntimeError as e:
                    logger.log("ERROR", f"Nie udało się uruchomić sniffera: {e}")
                    sys.exit(1)
                break
            else:
                logger.log("ERROR", f"Wprowadzony błędny numer interfejsu ('{choice}'). Wybierz liczbę całkowitą z zakresu 1-{sniffer.get_number_of_available_interfaces()}.")
        except ValueError:
            logger.log("ERROR", f"Wprowadzony błędny numer interfejsu ('{choice}'). Wybierz liczbę całkowitą z zakresu 1-{sniffer.get_number_of_available_interfaces()}.")
    #End loop

    logger.log("INFO", "Monitorowanie zakończone! Zamykam program.")


if __name__ == "__main__":
    main()
