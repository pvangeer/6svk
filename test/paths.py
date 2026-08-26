from pathlib import Path

# TODO: Maybe consider changing all file paths to a Path instead of string and passing Path variables.
test_data_dir = Path(__file__).parent / "test-data"

test_output_dir = Path(__file__).parent / "test-output"
test_output_dir.mkdir(parents=True, exist_ok=True)

base_dir = Path("C:/Users/geer/OneDrive - Stichting Deltares/Projecten/Kennisvragen SVK")
hv_dir = base_dir / "03 HV/01 Uitwerking"
mlk_dir = base_dir / "05 MLK/01 Uitwerking"
hk_dir = base_dir / "06 HK/01 Uitwerking"
rp_dir = base_dir / "07 RP/01 Uitwerking"
hijk_dir = base_dir / "02 HIJK/01 Uitwerking"
esb_dir = base_dir / "04 OSK/01 Uitwerking"
allsvk_dir = base_dir / "08 6SVK"
ssb_dir = Path(
    "C:/Users/geer/OneDrive - Stichting Deltares/Projecten/11212142 - NWO SSB Delta/General/C. Report - advise/Impact pathway and research agenda"
)

hv_database_path = hv_dir / "Eerste toepassing methodiek kennisvragen SVK HV_Concept.xlsx"
mlk_database_path = mlk_dir / "Concept Eerste toepassing methodiek kennisvragen SVK MLK.xlsx"
hk_database_path = hk_dir / "Concept Eerste toepassing methodiek kennisvragen SVK HK.xlsx"
rp_database_path = rp_dir / "Concept Eerste toepassing methodiek kennisvragen SVK RP.xlsx"
hijk_database_path = hijk_dir / "Concept Eerste toepassing methodiek kennisvragen SVK HIJK.xlsx"
esb_database_path = esb_dir / "Concept Eerste toepassing methodiek kennisvragen SVK OSK.xlsx"
ssb_database_path = ssb_dir / "SSB-delta_impact-pathway-database.xlsx"
