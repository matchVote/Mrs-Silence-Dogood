defmodule Dogood.UtilsTest do
  use ExUnit.Case

  test "normalize_date/1 converts nil into current DateTime" do
    result = Dogood.Utils.normalize_date(nil)
    assert %DateTime{} = result
  end

  test "normalize_date/1 converts a string of seconds into a DateTime" do
    result = Dogood.Utils.normalize_date("1476795294")
    assert %DateTime{} = result
    assert :lt == DateTime.compare(result, DateTime.utc_now())
  end

  test "normalize_date/1 converts an integer into a DateTime" do
    result = Dogood.Utils.normalize_date(1_476_795_294)
    assert %DateTime{} = result
    assert :lt == DateTime.compare(result, DateTime.utc_now())
  end

  test "normalize_date/1 returns a date string untouched" do
    assert "03/16/2018" == Dogood.Utils.normalize_date("03/16/2018")
  end

  test "normalize_date/1 returns a DateTime struct untouched" do
    now = DateTime.utc_now()
    assert now == Dogood.Utils.normalize_date(now)
  end
end
