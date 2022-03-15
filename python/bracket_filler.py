import game_picker
from pathlib import Path

PRINT_BLOCK_SIZE = 16
JUSTIFY_LEFT = 0
JUSTIFY_RIGHT = 1
JUSTIFY_CENTER = 2

def append_string(cur_string, new_string, append_to_left):
    return new_string + cur_string if append_to_left else cur_string + new_string

def format_bracket_string(str, fill_char, justify):
    if justify == JUSTIFY_LEFT:
        return str.ljust(PRINT_BLOCK_SIZE, fill_char)
    elif justify == JUSTIFY_RIGHT:
        return str.rjust(PRINT_BLOCK_SIZE, fill_char)
    else: # JUSTIFY_CENTER
        return str.center(PRINT_BLOCK_SIZE, fill_char)

class BracketFiller:
    bracket_64 = [[None]  * 16 for x in range(0,4)] # 16 teams per region, 4 regions
    bracket_32 = [[None]  * 8 for x in range(0,4)] # 8 teams per region, 4 regions
    bracket_16 = [[None]  * 4 for x in range(0,4)] # 4 teams per region, 4 regions
    bracket_8 = [[None]  * 2 for x in range(0,4)] # 2 teams per region, 4 regions
    bracket_4 = [None]  * 4 # Final 4, region winner in same index as its region in previous rounds
    bracket_2 = [None] * 2 # Championship
    bracket_champ = [None]
    bracket_full = [bracket_64, bracket_32, bracket_16, bracket_8, bracket_4, bracket_2, bracket_champ]


    def print_bracket(self):
        strings = [""] * 127
        string_pad = " " * PRINT_BLOCK_SIZE
        cur_string = 0
        
        cur_64_region = 0
        cur_64_team = 0
        cur_32_region = 0
        cur_32_team = 0
        cur_16_region = 0
        cur_16_team = 0
        cur_8_region = 0
        cur_8_team = 0
        cur_4_region = 0
        cur_2_region = 0
        for cur_string in range(0, 127):
            bracket_deco_justify = JUSTIFY_RIGHT if cur_string < 64 else JUSTIFY_LEFT
            # Populate every other string with round of 64
            if cur_string % 2 == 0:
                strings[cur_string] = format_bracket_string(self.bracket_64[cur_64_region][cur_64_team][0], '-', JUSTIFY_CENTER)
                if cur_64_team == 15:
                    cur_64_region += 1
                    cur_64_team = 0
                else:
                    cur_64_team += 1
             # Add bracket lines where necessary
            elif cur_string % 4 == 1:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string("|", ' ', bracket_deco_justify), cur_string >= 64)
            # Add spacing where necessary
            else:
                strings[cur_string] = string_pad

            # Populate every 4th string (offset by 1) with round of 32
            if cur_string % 4 == 1:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string(self.bracket_32[cur_32_region][cur_32_team][0], '-', JUSTIFY_CENTER), cur_string >= 64)
                if cur_32_team == 7:
                    cur_32_region += 1
                    cur_32_team = 0
                else:
                    cur_32_team += 1
            # Add bracket lines where necessary
            elif cur_string % 8 > 1 and cur_string % 8 < 5:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string("|", ' ', bracket_deco_justify), cur_string >= 64)
            # Add spacing where necessary
            else:
                strings[cur_string] = append_string(strings[cur_string], string_pad, cur_string >= 64)

            # Populate every 8th string (offset by 3)  with sweet 16
            if cur_string % 8 == 3:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string(self.bracket_16[cur_16_region][cur_16_team][0], '-', JUSTIFY_CENTER), cur_string >= 64)
                if cur_16_team == 3:
                    cur_16_region += 1
                    cur_16_team = 0
                else:
                    cur_16_team += 1
            # Add bracket lines where necessary
            elif cur_string % 16 > 3 and cur_string % 16 < 11:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string("|", ' ', bracket_deco_justify), cur_string >= 64)
            # Add spacing where necessary
            else:
                strings[cur_string] = append_string(strings[cur_string], string_pad, cur_string >= 64)

            # Populate every 16th string (offset by 7)  with elite 8
            if cur_string % 16 == 7:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string(self.bracket_8[cur_8_region][cur_8_team][0], '-', JUSTIFY_CENTER), cur_string >= 64)
                if cur_8_team == 1:
                    cur_8_region += 1
                    cur_8_team = 0
                else:
                    cur_8_team += 1
            # Add bracket lines where necessary
            elif cur_string % 32 > 7 and cur_string % 32 < 23:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string("|", ' ', bracket_deco_justify), cur_string >= 64)
            # Add spacing where necessary
            else:
                strings[cur_string] = append_string(strings[cur_string], string_pad, cur_string >= 64)

            # Populate every 32nd string (offset by 15)  with final 4
            if cur_string % 32 == 15:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string(self.bracket_4[cur_4_region][0], '-', JUSTIFY_CENTER), cur_string >= 64)
                cur_4_region += 1
            # Add bracket lines where necessary
            elif cur_string % 64 > 15 and cur_string % 64 < 47:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string("|", ' ', bracket_deco_justify), cur_string >= 64)
            # Add spacing where necessary
            else:
                strings[cur_string] = append_string(strings[cur_string], string_pad, cur_string >= 64)

            # Populate every 64th string (offset by 31)  with championship
            if cur_string % 64 == 31:
                strings[cur_string] = append_string(strings[cur_string], format_bracket_string(self.bracket_2[cur_2_region][0], '-', JUSTIFY_CENTER), cur_string >= 64)
                cur_2_region += 1
            else:
                strings[cur_string] = append_string(strings[cur_string], string_pad, cur_string >= 64)

            # Populate 31st row with champion
            if cur_string == 31:
                strings[cur_string] = append_string(strings[31], f"{self.bracket_champ[0][0]:^{PRINT_BLOCK_SIZE}}", False)
            # Add spacing where necessary
            elif cur_string < 63:
                strings[cur_string] = append_string(strings[cur_string], string_pad, False)



        print_filepath = Path(__file__).parent / "../data/bracket.txt"
        f = open(print_filepath, "w")

        for i in range(0, 63):
            f.write(strings[i] + strings[i + 64] + "\n")

    def read_bracket(self, csv_path):
        
        abs_path = Path(__file__).parent / csv_path
        f = open(abs_path)
        lines = f.readlines()
        cur_region = 0
        cur_team = 0
        for line in lines:
            line.rstrip()
            if cur_team > 15:
                cur_region += 1
                cur_team = 0
            team_data = line.split(',')
            team_data[1] = int(team_data[1])
            self.bracket_64[cur_region][cur_team] = team_data
            cur_team += 1
        
        #self.print_bracket()

    def fill_bracket(self):
        # Assumes bracket has already been read
        for x in range(0, len(self.bracket_full) - 1):
            cur_round = self.bracket_full[x]
            next_round = self.bracket_full[x + 1]
            for region in range(0, 4):
                # Set iteration range to cover rounds withe arrays per region (Elite 8 and earlier)
                # and with single arrays (Final 4 and championship)
                round_range = len(cur_round[region]) if x <= 3 else len(cur_round)

                for y in range(0, round_range, 2):
                    if x < 3: # Structure for first 3 rounds is array of arrays
                        next_round[region][int (y / 2)] = game_picker.pickgame(cur_round[region][y], cur_round[region][y + 1])
                    elif x == 3: # Consolidate from array per region to single Final 4 array
                        next_round[region] = game_picker.pickgame(cur_round[region][y], cur_round[region][y + 1])
                    else:
                        next_round[int(y / 2)] = game_picker.pickgame(cur_round[y], cur_round[y + 1])

    

if __name__ == "__main__":
    bkt = BracketFiller()
    bkt.read_bracket("../data/ncaa_mens_2022.csv")
    bkt.fill_bracket()
    bkt.print_bracket()