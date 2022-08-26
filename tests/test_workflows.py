# moved from test_ytschema, need to modify to work with new workflow
# def test_execution():
#
#     # we can inject an instantiated dataset here! the methods that require a
#     # ds will check the dataset store if ds is None and use this ds:
#     test_ds = fake_amr_ds(fields=[("gas", "temperature")], units=["K"])
#     dataset_fixture._instantiated_datasets["_test_ds"] = test_ds
#
#     # run the slice plot
#     model = analysis_schema.ytModel.parse_raw(viz_only_slc)
#     m = model._run()
#     print(m)
#     assert isinstance(m[0], yt.AxisAlignedSlicePlot)
#
#     # run the projection plot
#     model = analysis_schema.ytModel.parse_raw(viz_only_prj)
#     m = model._run()
#     print(m)
#     assert isinstance(m[0], yt.ProjectionPlot)
