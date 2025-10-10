import csv
import os

def get_penguins(f):
    with open(f, newline='') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    if not rows or len(rows) < 2:
        return {}

    headers = rows[0][1:]
    d = {category: {} for category in headers}

    for row in rows[1:]:
        penguin = row[0]
        for i, category in enumerate(headers):
            value = row[i + 1]
            try:
                d[category][penguin] = float(value)
            except ValueError:
                d[category][penguin] = value
    return d


def get_bill_depths(d):
    bill_depths = []
    for category, penguins in d.items():
        for penguin, row in penguins.items():
            depth = row.get('bill_depth-mm')
            if depth not in (None, '', 'NA'):
                try:
                    bill_depths.append(float(depth))
                except ValueError:
                    pass
    return bill_depths

def get_average_bill_depths(penguin_dict):
    """Return a dictionary of average bill depths per species (in mm)."""
    averages = {}
    for species, penguins in penguin_dict.items():
        depths = [
            p["bill_depth_mm"]
            for p in penguins.values()
            if "bill_depth_mm" in p and isinstance(p["bill_depth_mm"], (int, float))
        ]
        if depths:
            averages[species] = sum(depths) / len(depths)
        else:
            averages[species] = None  # no valid values
    return averages

def locate_above_avg(bill_depths, averages):
    """
    Compare each penguin's bill depth to the mean for its species.
    Return a list of body masses (in g) for penguins above the mean.
    """
    above_avg_masses = []

    for penguin in bill_depths:
        species = penguin.get("species")
        bill_depth = penguin.get("bill_depth_mm")
        mass = penguin.get("body_mass_g")

        # Only proceed if data is valid and species mean exists
        if (
            species in averages
            and isinstance(bill_depth, (int, float))
            and isinstance(mass, (int, float))
        ):
            if bill_depth > averages[species]:
                above_avg_masses.append(mass)

    return above_avg_masses


def finalize_report(averages, masses, filename="penguin_report.txt"):
    """
    Writes a report summarizing average bill depths and above-average body masses.

    Parameters:
        means (dict): average bill depths per species.
        masses (list): body masses (g) of penguins above the average.
        filename (str): output file name (default 'penguin_report.txt').

    Output:
        Writes to a text file; returns nothing.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    report_path = os.path.join(base_path, filename)

    with open(report_path, "w") as f:
        f.write("Penguin Bill Depth Report\n")
        f.write("=========================\n\n")
        f.write("Average Bill Depths (mm):\n")

        if not averages:
            f.write("No data available.\n")
        else:
            for species, avg in averages.items():
                f.write(f" - {species}: {avg:.2f} mm\n")

        f.write("\nBody Masses of Penguins Above Average Depth:\n")

        if masses:
            f.write(", ".join([str(m) + "g" for m in masses]) + "\n")
        else:
            f.write("None\n")

def main():
    """
    Runs the penguin analysis program.
    Reads data, computes averages, identifies above-average penguins,
    and writes a final report to a file.
    """
    # Step 1: Load penguin data
    csv_file = "penguins.csv"  # make sure this file is in the same folder
    penguins = get_penguins(csv_file)
    print("✅ Data successfully loaded!")

    # Step 2: Calculate average bill depths
    means = get_average_bill_depths(penguins)
    print("✅ Computed average bill depths per species.")

    # Step 3: Build a list of penguin records (species, bill_depth, body_mass)
    depths = []
    for species, penguin_group in penguins.items():
        for penguin_id, data in penguin_group.items():
            try:
                bill_depth = float(data.get("bill_depth_mm", "nan"))
                body_mass = float(data.get("body_mass_g", "nan"))
            except (TypeError, ValueError):
                continue  # skip if missing or invalid
            depths.append({
                "species": species,
                "bill_depth_mm": bill_depth,
                "body_mass_g": body_mass
            })
    print(f"✅ Created {len(depths)} penguin depth records.")

    # Step 4: Locate penguins with above-average bill depths
    masses = locate_above_avg(depths, means)
    print(f"✅ Found {len(masses)} penguins with above-average bill depths.")

    # Step 5: Write the final report
    finalize_report(means, masses)
    print("📄 Final report successfully written to 'penguin_report.txt'!")

if __name__ == "__main__":
    main()
