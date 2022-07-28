from os import system, name

from calculator_service import calculatorService as calc

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


class CalculatorUI:
    def __init__(self):
        clear()

    def _close(self):
        print("Suljetaan...")
        exit()

    def _print_coordinates(self):
        print()
        confirm_str = "KOORDINAATIT"
        print(confirm_str)
        print("-"*len(confirm_str))
        print(f"Heitin:\t\t{calc.get_coords('mortar')[0]:05d} {calc.get_coords('mortar')[1]:05d}")
        print(f"Kohde:\t\t{calc.get_coords('target')[0]:05d} {calc.get_coords('target')[1]:05d}")
        print(f"Tulenjohtaja:\t{calc.get_coords('observer')[0]:05d} {calc.get_coords('observer')[1]:05d}")
        print()


    def _print_firing_values(self):
        print()
        solution_str = "HEITTIMEN ARVOT"
        if calc.range_table_set:
            solution_str = solution_str + " " + calc.range_table_name
        print(solution_str)
        print("-"*len(solution_str))
        if calc.coords_set("mortar") and calc.coords_set("target"):
            az = round(calc.get_az_to_target())

            if calc.range_table_set:
                try:
                    charge, elev, tof = calc.get_elev_to_target()
                    print(f"Panos: {charge}")
                    print(f"Sivu: {az//100:02d}-{az%100:02d}")
                    print(f"Koro: {elev:.0f}")
                    print(f"Lentoaika: {tof:.1f}s")
                except ValueError:
                    print("ETÄISYYS EI MAHDOLLINEN!")
            else:
                print(f"Sivu: {az//100:02d}-{az%100:02d}")
                print(f"Etäisyys: {calc.get_dist_to_target():.0f}m")
        else:
            if calc.range_table_set:
                print(f"Panos: ---")
                print(f"Sivu: ---")
                print(f"Koro: ---")
                print(f"Lentoaika: ---")
            else:
                print(f"Sivu: ---")
                print(f"Etäisyys: ---")
        print()

    def _update_firing_values(self):
        while True:
            clear()
            print("Aseta heittimen sijainti syöttämällä 'H' ja koordinaatit.")
            print("Aseta kohde syöttämällä 'K' ja koordinaatit, tai pelkät koordinaatit.")
            print("Aseta tulenjohtajan sijainti syöttämällä 'T' ja koordinaatit.")
            if calc.coords_set("observer"):
                print("Anna korjaukset muodossa \"X(V/O) ja/tai Y(J/L)\".")
            print("Paina 'N' nollataksesi. Paina 'S' sulkeaksesi.")

            self._print_coordinates()
            self._print_firing_values()

            action_str = input("Syöte: ")

            if not action_str:
                continue

            if action_str.upper() == "S":
                self._close()
            if action_str.upper() == "N":
                clear()
                calc.zero_values()

            try:
                int(action_str[0])
                action_str = "K" + action_str
            except ValueError:
                pass


            pos_name = None
            if action_str[0].upper() == "H":
                pos_name = "mortar"
            if action_str[0].upper() == "K":
                pos_name = "target"
            if action_str[0].upper() == "T":
                pos_name = "observer"

            if pos_name:
                try:
                    calc.set_coords(action_str[1:], pos_name)
                except ValueError:
                    pass

            try:
                calc.update_target(action_str)
            except ValueError:
                pass

    def get_range_table(self):
        while True:
            range_table_path = input("Taulukon tiedostonimi (valinnainen): ")
            if range_table_path:
                calc.set_range_table(range_table_path)
                try:
                    calc.set_range_table(range_table_path)
                    break
                except:
                    print("Väärä tiedostonimi TAI virheellinen taulukko!")
                    continue
            else:
                break

    def run(self):
        self.get_range_table()
        while True:
            try:
                self._update_firing_values()
            except ValueError:
                clear()
                calc.zero_values()

calculator = CalculatorUI()
